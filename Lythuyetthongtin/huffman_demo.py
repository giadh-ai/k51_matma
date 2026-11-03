"""Interactive Huffman and Shannon-Fano coding demonstration."""

from __future__ import annotations

import heapq
import html
import math
from collections import Counter
from dataclasses import dataclass

import gradio as gr


@dataclass
class Node:
    """A leaf or an internal node in a prefix-code tree."""

    frequency: int
    symbol: str | None = None
    left: Node | None = None
    right: Node | None = None
    label: str = ""


def display_symbol(symbol: str) -> str:
    """Return a readable label for a character, including whitespace."""
    special = {
        " ": "␠",
        "\n": "\\n",
        "\r": "\\r",
        "\t": "\\t",
    }
    if symbol in special:
        return special[symbol]
    if symbol.isprintable():
        return symbol
    return f"U+{ord(symbol):04X}"


def html_table(headers: list[str], rows: list[list[str]]) -> str:
    """Build a small escaped HTML table for a Gradio Markdown component."""
    header_html = "".join(f"<th>{html.escape(value)}</th>" for value in headers)
    row_html = "\n".join(
        "<tr>" + "".join(f"<td>{html.escape(value)}</td>" for value in row) + "</tr>"
        for row in rows
    )
    return (
        '<table><thead><tr>'
        f"{header_html}"
        "</tr></thead><tbody>"
        f"{row_html}"
        "</tbody></table>"
    )


def frequencies_for(text: str) -> tuple[Counter[str], dict[str, int]]:
    """Count Unicode code points and remember their first appearance."""
    if not text:
        raise ValueError("Vui lòng nhập ít nhất một ký tự.")
    return Counter(text), {symbol: index for index, symbol in enumerate(dict.fromkeys(text))}


def source_entropy(frequencies: Counter[str]) -> float:
    """Calculate the source entropy in bits per character."""
    total = sum(frequencies.values())
    return -sum(
        (count / total) * math.log2(count / total)
        for count in frequencies.values()
    )


def frequency_report(text: str, frequencies: Counter[str], first_seen: dict[str, int]) -> str:
    total = len(text)
    entropy = source_entropy(frequencies)
    rows = []
    for symbol in sorted(frequencies, key=lambda item: first_seen[item]):
        probability = frequencies[symbol] / total
        self_information = -math.log2(probability)
        contribution = probability * self_information
        rows.append(
            [
                display_symbol(symbol),
                str(frequencies[symbol]),
                f"{probability:.6f}",
                f"{self_information:.6f}",
                f"{contribution:.6f}",
            ]
        )
    rows.append(["Tổng cộng", str(total), "1.000000", "—", f"{entropy:.6f}"])
    return (
        "## Bước 1: Tính tần suất xuất hiện\n"
        "Mỗi ký tự Unicode được đếm riêng; khoảng trắng và ký tự xuống dòng "
        "được hiển thị lần lượt là `␠` và `\\n`.\n\n"
        "Entropy riêng của ký tự được tính bằng `I(x) = -log₂(p(x))`; "
        "đóng góp vào entropy nguồn là `p(x) × I(x)`. "
        "Entropy trung bình `H(X) = Σ p(x)I(x)`.\n\n"
        + html_table(
            [
                "Ký tự",
                "Tần suất",
                "Xác suất p(x)",
                "I(x) (bit)",
                "Đóng góp p(x)I(x) (bit)",
            ],
            rows,
        )
        + f"\n\n**Entropy trung bình của nguồn: {entropy:.6f} bit/ký tự.**"
    )


def format_node(node: Node) -> str:
    label = display_symbol(node.symbol) if node.symbol is not None else node.label
    return f"({label}:{node.frequency})"


def queue_listing(heap: list[tuple[int, int, Node]]) -> str:
    ordered = sorted(heap, key=lambda item: (item[0], item[1]))
    return "[" + ", ".join(format_node(item[2]) for item in ordered) + "]"


def assign_tree_codes(node: Node, prefix: str, codes: dict[str, str]) -> None:
    if node.symbol is not None:
        codes[node.symbol] = prefix or "0"
        return
    if node.left is not None:
        assign_tree_codes(node.left, prefix + "0", codes)
    if node.right is not None:
        assign_tree_codes(node.right, prefix + "1", codes)


def tree_as_svg(root: Node) -> str:
    """Render the prefix tree as a scrollable SVG diagram."""
    leaf_positions: dict[int, float] = {}
    depths: dict[int, int] = {}
    node_positions: dict[int, tuple[float, float]] = {}
    leaf_index = 0
    horizontal_gap = 108
    left_margin = 58
    top_margin = 52
    vertical_gap = 104

    def measure(node: Node, depth: int) -> float:
        nonlocal leaf_index
        depths[id(node)] = depth
        if node.symbol is not None:
            x = left_margin + leaf_index * horizontal_gap
            leaf_index += 1
        else:
            child_positions = [
                measure(child, depth + 1)
                for child in (node.left, node.right)
                if child is not None
            ]
            x = sum(child_positions) / len(child_positions)
        leaf_positions[id(node)] = x
        return x

    measure(root, 0)
    max_depth = max(depths.values(), default=0)
    for node_id, x in leaf_positions.items():
        node_positions[node_id] = (x, top_margin + depths[node_id] * vertical_gap)

    width = max(160, left_margin * 2 + max(leaf_index - 1, 0) * horizontal_gap)
    height = top_margin * 2 + max_depth * vertical_gap
    edge_markup: list[str] = []
    node_markup: list[str] = []

    def draw(node: Node) -> None:
        x, y = node_positions[id(node)]
        label = display_symbol(node.symbol) if node.symbol is not None else node.label

        for bit, child in (("0", node.left), ("1", node.right)):
            if child is None:
                continue
            child_x, child_y = node_positions[id(child)]
            edge_markup.append(
                f'<line x1="{x:g}" y1="{y + 28:g}" x2="{child_x:g}" '
                f'y2="{child_y - 28:g}" class="tree-edge"/>'
            )
            label_x = (x + child_x) / 2
            label_y = (y + child_y) / 2
            edge_markup.append(
                f'<rect x="{label_x - 10:g}" y="{label_y - 11:g}" '
                'width="20" height="20" rx="8" class="bit-bg"/>'
            )
            edge_markup.append(
                f'<text x="{label_x:g}" y="{label_y + 4:g}" '
                'text-anchor="middle" class="edge-label">'
                f"{bit}</text>"
            )
            draw(child)

        if node.symbol is None:
            node_markup.append(
                f'<circle cx="{x:g}" cy="{y:g}" r="29" class="internal-node"/>'
            )
            node_markup.append(
                f'<text x="{x:g}" y="{y - 2:g}" text-anchor="middle" '
                f'class="node-label">{html.escape(label)}</text>'
            )
            node_markup.append(
                f'<text x="{x:g}" y="{y + 15:g}" text-anchor="middle" '
                f'class="frequency-label">{node.frequency}</text>'
            )
        else:
            node_markup.append(
                f'<rect x="{x - 39:g}" y="{y - 25:g}" width="78" height="50" '
                'rx="12" class="leaf-node"/>'
            )
            node_markup.append(
                f'<text x="{x:g}" y="{y - 3:g}" text-anchor="middle" '
                f'class="node-label">{html.escape(label)}</text>'
            )
            node_markup.append(
                f'<text x="{x:g}" y="{y + 15:g}" text-anchor="middle" '
                f'class="frequency-label">{node.frequency}</text>'
            )

    draw(root)
    return (
        '<div style="overflow-x:auto;max-width:100%;border:1px solid #e5e7eb;'
        'border-radius:8px;padding:8px;background:#fff">'
        f'<svg xmlns="http://www.w3.org/2000/svg" role="img" '
        f'aria-label="Cây mã Huffman hoặc Shannon–Fano, {leaf_index} ký tự" '
        f'viewBox="0 0 {width} {height}" width="{width}" height="{height}" '
        'style="display:block;max-width:none">'
        '<style>'
        '.tree-edge{stroke:#64748b;stroke-width:2}'
        '.bit-bg{fill:#fff}'
        '.edge-label{font:700 13px sans-serif;fill:#2563eb}'
        '.internal-node{fill:#eff6ff;stroke:#3b82f6;stroke-width:2}'
        '.leaf-node{fill:#f0fdf4;stroke:#22c55e;stroke-width:2}'
        '.node-label{font:600 13px sans-serif;fill:#111827}'
        '.frequency-label{font:12px sans-serif;fill:#4b5563}'
        '</style>'
        f'{"".join(edge_markup)}{"".join(node_markup)}'
        "</svg></div>"
    )


def huffman(
    frequencies: Counter[str], first_seen: dict[str, int]
) -> tuple[dict[str, str], str, Node]:
    ordered_symbols = sorted(
        frequencies,
        key=lambda symbol: (frequencies[symbol], first_seen[symbol]),
    )
    heap: list[tuple[int, int, Node]] = []
    serial = 0
    for symbol in ordered_symbols:
        leaf = Node(frequency=frequencies[symbol], symbol=symbol)
        heapq.heappush(heap, (leaf.frequency, serial, leaf))
        serial += 1

    initial_queue = queue_listing(heap)
    steps = [
        "## Bước 2: Mã hóa Huffman (từ dưới lên)",
        f"Khởi tạo, sắp xếp theo tần suất tăng dần: `{initial_queue}`",
    ]
    merge_number = 1

    while len(heap) > 1:
        first_frequency, _, left = heapq.heappop(heap)
        second_frequency, _, right = heapq.heappop(heap)
        parent = Node(
            frequency=first_frequency + second_frequency,
            left=left,
            right=right,
            label=f"N{merge_number}",
        )
        heapq.heappush(heap, (parent.frequency, serial, parent))
        serial += 1
        steps.append(
            f"{merge_number}. Kết hợp: chọn `{format_node(left)}` và "
            f"`{format_node(right)}`; tạo `{format_node(parent)}`. "
            f"Quy ước `{format_node(left)}` = 0, `{format_node(right)}` = 1.\n"
            f"   Danh sách: `{queue_listing(heap)}`"
        )
        merge_number += 1

    root = heap[0][2]
    root.label = "Gốc"
    codes: dict[str, str] = {}
    assign_tree_codes(root, "", codes)
    return codes, "\n\n".join(steps), root


def shannon_fano(
    frequencies: Counter[str], first_seen: dict[str, int]
) -> tuple[dict[str, str], str, Node]:
    ordered_symbols = sorted(
        frequencies,
        key=lambda symbol: (-frequencies[symbol], first_seen[symbol]),
    )
    codes: dict[str, str] = {}
    steps = ["## Bước 3: Mã hóa Shannon–Fano (từ trên xuống)"]
    node_number = 1

    def build(symbols: list[str], prefix: str, depth: int) -> Node:
        nonlocal node_number
        indent = "  " * depth
        group = ", ".join(
            f"{display_symbol(symbol)}:{frequencies[symbol]}" for symbol in symbols
        )
        if len(symbols) == 1:
            symbol = symbols[0]
            codes[symbol] = prefix or "0"
            steps.append(
                f"{indent}- Nhóm [{group}] là ký tự đơn; mã là `{codes[symbol]}`."
            )
            return Node(frequency=frequencies[symbol], symbol=symbol)

        total = sum(frequencies[symbol] for symbol in symbols)
        left_frequency = 0
        split_index = 1
        smallest_difference = total + 1
        for index, symbol in enumerate(symbols[:-1], start=1):
            left_frequency += frequencies[symbol]
            difference = abs(total - 2 * left_frequency)
            if difference < smallest_difference:
                split_index = index
                smallest_difference = difference

        left_symbols = symbols[:split_index]
        right_symbols = symbols[split_index:]
        left_frequency = sum(frequencies[symbol] for symbol in left_symbols)
        right_frequency = total - left_frequency
        steps.append(
            f"{indent}- Nhóm [{group}], tổng {total}: chia thành "
            f"[{', '.join(display_symbol(symbol) for symbol in left_symbols)}] "
            f"({left_frequency}) = 0 và "
            f"[{', '.join(display_symbol(symbol) for symbol in right_symbols)}] "
            f"({right_frequency}) = 1."
        )
        left = build(left_symbols, prefix + "0", depth + 1)
        right = build(right_symbols, prefix + "1", depth + 1)
        parent = Node(
            frequency=total,
            left=left,
            right=right,
            label=f"S{node_number}",
        )
        node_number += 1
        return parent

    root = build(ordered_symbols, "", 0)
    root.label = "Gốc"
    return codes, "\n".join(steps), root


def code_table(
    frequencies: Counter[str], first_seen: dict[str, int], codes: dict[str, str]
) -> str:
    rows = [
        [
            display_symbol(symbol),
            str(frequencies[symbol]),
            codes[symbol],
        ]
        for symbol in sorted(frequencies, key=lambda item: first_seen[item])
    ]
    return html_table(["Ký tự", "Tần suất", "Mã"], rows)


def algorithm_result(
    title: str,
    text: str,
    frequencies: Counter[str],
    first_seen: dict[str, int],
    codes: dict[str, str],
    tree: Node,
) -> tuple[str, str]:
    encoded = "".join(codes[symbol] for symbol in text)
    original_bits = len(text.encode("utf-8")) * 8
    encoded_bits = len(encoded)
    saved_bits = original_bits - encoded_bits
    reduction_percent = saved_bits / original_bits * 100 if original_bits else 0.0
    source_h = source_entropy(frequencies)
    average_code_length = sum(
        (frequencies[symbol] / len(text)) * len(codes[symbol])
        for symbol in frequencies
    )
    coding_efficiency = source_h / average_code_length * 100 if average_code_length else 0.0
    redundancy = average_code_length - source_h
    if title.endswith("Huffman"):
        optimality = (
            "Huffman đạt độ dài mã trung bình tối ưu trong các mã tiền tố nhị phân "
            "cho phân phối ký tự này."
        )
    else:
        optimality = (
            "Shannon–Fano là cách xây dựng gần tối ưu nhưng không đảm bảo độ dài "
            "mã trung bình nhỏ nhất; so sánh L̄ với H(X) để đánh giá."
        )
    if len(frequencies) == 1:
        optimality += (
            " Với một ký tự duy nhất, chương trình gán mã `0` (1 bit/ký tự) "
            "để chuỗi vẫn có biểu diễn rõ ràng."
        )
    report = (
        f"## {title}\n"
        "### So sánh kích thước\n"
        f"- Trước mã hóa (chuỗi UTF-8, 8 bit/byte): **{original_bits} bit**\n"
        f"- Sau mã hóa (chỉ tính chuỗi mã): **{encoded_bits} bit**\n"
        f"- Chênh lệch: **{saved_bits:+d} bit**\n"
        f"- Tỷ lệ giảm so với dữ liệu UTF-8 ban đầu: **{reduction_percent:.2f}%**\n"
        f"- Kích thước mã / kích thước ban đầu: **"
        f"{(encoded_bits / original_bits * 100) if original_bits else 0.0:.2f}%**\n\n"
        "### Đánh giá theo entropy\n"
        f"- Entropy nguồn `H(X)`: **{source_h:.6f} bit/ký tự**\n"
        f"- Độ dài mã trung bình `L̄`: **{average_code_length:.6f} bit/ký tự**\n"
        f"- Dư thừa `L̄ − H(X)`: **{redundancy:.6f} bit/ký tự**\n"
        f"- Hiệu suất mã hóa `H(X) / L̄`: **{coding_efficiency:.2f}%**\n"
        f"- {optimality}\n\n"
        "> So sánh kích thước chưa tính phần lưu bảng mã/tần suất và các chi phí "
        "đóng gói bit; chuỗi mã đang được tính theo từng bit.\n\n"
        "### Bảng mã\n"
        f"{code_table(frequencies, first_seen, codes)}\n\n"
        "### Chuỗi bit đã mã hóa\n"
        f"```text\n{encoded}\n```"
    )
    diagram = (
        "<h3>Cây mã (nhánh trái = 0, nhánh phải = 1)</h3>"
        + tree_as_svg(tree)
    )
    return report, diagram


def build_demo_report(text: str) -> tuple[str, str, str, str, str, str, str]:
    """Create the frequency, algorithm-step, and encoded-result reports."""
    if not text:
        raise gr.Error("Vui lòng nhập ít nhất một ký tự để mã hóa.")

    frequencies, first_seen = frequencies_for(text)
    huffman_codes, huffman_steps, huffman_tree = huffman(frequencies, first_seen)
    shannon_codes, shannon_steps, shannon_tree = shannon_fano(frequencies, first_seen)

    return (
        frequency_report(text, frequencies, first_seen),
        huffman_steps,
        *algorithm_result(
            "Kết quả Huffman",
            text,
            frequencies,
            first_seen,
            huffman_codes,
            huffman_tree,
        ),
        shannon_steps,
        *algorithm_result(
            "Kết quả Shannon–Fano",
            text,
            frequencies,
            first_seen,
            shannon_codes,
            shannon_tree,
        ),
    )


with gr.Blocks(title="Minh họa mã hóa Huffman và Shannon–Fano") as demo:
    gr.Markdown(
        """
        # Minh họa mã hóa Huffman và Shannon–Fano

        Nhập chuỗi cần mã hóa. Ứng dụng sẽ đếm tần suất từng ký tự, trình bày
        các bước xây dựng mã và tạo chuỗi bit cho cả hai thuật toán.
        """
    )
    input_text = gr.Textbox(
        label="Chuỗi đầu vào",
        value="ABRACADABRA",
        lines=4,
        placeholder="Nhập văn bản, bao gồm dấu cách hoặc ký tự tiếng Việt...",
    )
    encode_button = gr.Button("Phân tích và mã hóa", variant="primary")
    frequency_output = gr.Markdown()

    with gr.Tabs():
        with gr.Tab("Huffman"):
            huffman_steps_output = gr.Markdown()
            huffman_result_output = gr.Markdown()
            huffman_tree_output = gr.HTML()
        with gr.Tab("Shannon–Fano"):
            shannon_steps_output = gr.Markdown()
            shannon_result_output = gr.Markdown()
            shannon_tree_output = gr.HTML()

    encode_button.click(
        fn=build_demo_report,
        inputs=input_text,
        outputs=[
            frequency_output,
            huffman_steps_output,
            huffman_result_output,
            huffman_tree_output,
            shannon_steps_output,
            shannon_result_output,
            shannon_tree_output,
        ],
    )


if __name__ == "__main__":
    demo.launch()
