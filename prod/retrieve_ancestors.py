from stsp import line_to_vertex
from ancestors import is_ancestor


def retrieve_ancestors(k: int):
    anc_lines = ["n,xi\n"]

    # Retrieve vertices for n in range(k + 3, 2 * k + 1)
    for n in range(k + 3, 2 * k + 1):
        with open(f"../vertices/vertices_{n}.txt", 'r') as f:
            vert_lines = f.readlines()

        # Check if the vertex is an ancestor of order k
        for line in vert_lines:
            if is_ancestor(n, line_to_vertex(n, line), k):
                anc_lines.append(f"{n},{line.strip()}\n")

    # Write the ancestors to a CSV file
    with open(f"../ancestors/ancestorssss_{k}.csv", 'w') as f:
        f.writelines(anc_lines)


if __name__ == "__main__":
    for k in range(3, 7):
        print(f"Retrieving ancestors of order {k}...")
        retrieve_ancestors(k)
