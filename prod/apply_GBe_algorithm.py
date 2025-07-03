from stsp import line_to_vertex
from GB_algorithm import GBe_algorithm


def apply_GBe_algorithm(k: int):
    # Retrieve the ancestors of order k
    with open(f"../ancestors/ancestors_{k}.csv", 'r') as f:
        vert_lines = f.readlines()
    vert_lines.pop(0)

    lines = "n,x0,gapII,family_gapII,num_it\n"

    for line in vert_lines:
        line_arr = line.strip().split(',')
        n = int(line_arr[0])
        x0 = line_to_vertex(n, line_arr[1])

        # Apply the GBe algorithm on vertex x0
        gapII, family_gapII, iterations = GBe_algorithm(n, x0, 4 / 3)

        lines += f"{line.strip()},{gapII:.6f},{family_gapII:.6f},{iterations}\n"

    # Write the results to a CSV file
    with open(f"output/GBe_on_ancestors_{k}.csv", 'w+') as f:
        f.write(lines)


if __name__ == "__main__":
    for k in range(3, 6):
        print(f"Applying GBe algorithm on ancestors of order {k}...")
        apply_GBe_algorithm(k)
