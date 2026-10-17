#!/usr/bin/env python3
"""Read the package attribute from Android's compiled binary AndroidManifest.xml."""
from __future__ import annotations
import argparse
import struct
import zipfile
from pathlib import Path

RES_STRING_POOL_TYPE = 0x0001
RES_XML_TYPE = 0x0003
RES_XML_START_ELEMENT_TYPE = 0x0102


def u16(buf: bytes, off: int) -> int:
    return struct.unpack_from('<H', buf, off)[0]


def u32(buf: bytes, off: int) -> int:
    return struct.unpack_from('<I', buf, off)[0]


def read_len8(buf: bytes, off: int) -> tuple[int, int]:
    first = buf[off]
    if first & 0x80:
        return ((first & 0x7f) << 8) | buf[off + 1], off + 2
    return first, off + 1


def read_len16(buf: bytes, off: int) -> tuple[int, int]:
    first = u16(buf, off)
    if first & 0x8000:
        return ((first & 0x7fff) << 16) | u16(buf, off + 2), off + 4
    return first, off + 2


def decode_string_pool(chunk: bytes) -> list[str]:
    header_size = u16(chunk, 2)
    string_count = u32(chunk, 8)
    flags = u32(chunk, 16)
    strings_start = u32(chunk, 20)
    utf8 = bool(flags & 0x100)
    result: list[str] = []
    for i in range(string_count):
        pos = strings_start + u32(chunk, header_size + 4 * i)
        if utf8:
            _, pos = read_len8(chunk, pos)
            byte_len, pos = read_len8(chunk, pos)
            result.append(chunk[pos:pos + byte_len].decode('utf-8', errors='replace'))
        else:
            char_len, pos = read_len16(chunk, pos)
            result.append(chunk[pos:pos + char_len * 2].decode('utf-16le', errors='replace'))
    return result


def parse_manifest_package(data: bytes) -> str:
    if len(data) < 8 or u16(data, 0) != RES_XML_TYPE:
        raise ValueError('AndroidManifest.xml is not a recognized binary XML document')
    off = u16(data, 2)
    strings: list[str] = []
    while off + 8 <= len(data):
        chunk_type, _header_size, chunk_size = struct.unpack_from('<HHI', data, off)
        if chunk_size < 8 or off + chunk_size > len(data):
            raise ValueError(f'Invalid XML chunk at offset {off}')
        chunk = data[off:off + chunk_size]
        if chunk_type == RES_STRING_POOL_TYPE:
            strings = decode_string_pool(chunk)
        elif chunk_type == RES_XML_START_ELEMENT_TYPE and strings:
            name_idx = u32(chunk, 20)
            tag = strings[name_idx] if name_idx < len(strings) else ''
            if tag == 'manifest':
                attribute_start = u16(chunk, 24)
                attribute_size = u16(chunk, 26)
                attribute_count = u16(chunk, 28)
                base = u16(chunk, 2) + attribute_start
                for i in range(attribute_count):
                    a = base + i * attribute_size
                    name_idx = u32(chunk, a + 4)
                    raw_idx = u32(chunk, a + 8)
                    value_type = chunk[a + 15]
                    value_data = u32(chunk, a + 16)
                    name = strings[name_idx] if name_idx < len(strings) else ''
                    if name == 'package':
                        if raw_idx != 0xffffffff and raw_idx < len(strings):
                            return strings[raw_idx]
                        if value_type == 0x03 and value_data < len(strings):
                            return strings[value_data]
                        return str(value_data)
        off += chunk_size
    raise ValueError('Could not find manifest package attribute')


def read_apk_package(apk: Path) -> str:
    with zipfile.ZipFile(apk) as zf:
        return parse_manifest_package(zf.read('AndroidManifest.xml'))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('apk', type=Path)
    parser.add_argument('--expect', help='Fail unless the package matches this value')
    args = parser.parse_args()
    package = read_apk_package(args.apk)
    print(package)
    if args.expect and package != args.expect:
        print(f'Expected {args.expect}, found {package}')
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
