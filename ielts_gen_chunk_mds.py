import csv
import os

# Fixed column setting - always use 1 column
cols = 1

# 读取 chunks.csv，建立 id -> (meaning, chunks) 映射
def read_chunks(filename):
    chunks_dict = {}
    with open(filename, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cid = int(row['id'])
            meaning = row['meanings']
            chunks = row['chunks']
            chunks_dict[cid] = (meaning, chunks)
    return chunks_dict

# 读取 location_chunks.csv，建立 location -> [chunk_ids] 映射
def read_location_chunks(filename):
    loc_chunks = {}
    with open(filename, encoding='utf-8') as f:
        reader = csv.reader(f)  # 使用 csv.reader 而不是 DictReader
        header = next(reader)  # 跳过表头
        for row in reader:
            if len(row) >= 2:  # 确保有足够的列
                location = row[0]
                # 将剩余的列作为 chunk_ids
                chunk_ids = [int(x.strip()) for x in row[1:] if x.strip().isdigit()]
                print(f"Location: {location}, Chunk IDs: {chunk_ids}")
                loc_chunks[location] = chunk_ids
    return loc_chunks

# 按顺序的写作段落
writing_order = [
    'T1P1',
    'T1P2',
    'T1P3',
    'T1C',
    'T2P1',
    'T2P2',
    'T2P3',
    'T2C',
]

def generate_md_lines(chunk_ids, chunks_dict):
    # Single column table header
    header = "| ID | Meaning | Chunks |"
    divider = "|----|---------|--------|"
    
    md_lines = [header, divider]

    # Generate rows for single column layout
    for cid in chunk_ids:
        if cid in chunks_dict:
            meaning, chunks = chunks_dict[cid]
            md_lines.append(f"| {cid} | {meaning} | {chunks} |")
        else:
            md_lines.append(f"| {cid} | (No data) | (No data) |")
    
    return md_lines

def main():
    input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "csv")

    chunks_file = os.path.join(input_dir, 'chunks.csv')
    location_chunks_file = os.path.join(input_dir, 'location_chunks.csv')

    chunks_dict = read_chunks(chunks_file)
    loc_chunks = read_location_chunks(location_chunks_file)

    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "md")
    output_dir = os.path.join(output_dir, "chunks")
    os.makedirs(output_dir, exist_ok=True)

    for idx, loc in enumerate(writing_order, start=1):
        md_name = f"{idx}_{loc}.md"
        md_path = os.path.join(output_dir, md_name)

        if loc not in loc_chunks:
            print(f"Warning: {loc} not found in location_chunks.csv")
            continue

        chunk_ids = loc_chunks[loc]
        md_lines = generate_md_lines(chunk_ids, chunks_dict)

        with open(md_path, "w", encoding="utf-8") as f:
            f.write(f"### {loc}\n\n")
            f.write("\n".join(md_lines))
            f.write("\n")

    print(f"共生成 {len(writing_order)} 个Markdown文件，保存在 {output_dir}")

if __name__ == "__main__":
    main()
