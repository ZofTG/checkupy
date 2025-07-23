import argparse
import json
import pandas as pd
from checkupy.checkupy import CheckupBIA


def run_bia(params, output_file):
    bia = CheckupBIA(**params)
    out = []
    for i, v in bia.to_dict().items():
        line = pd.DataFrame(pd.Series(v)).T
        line.index = pd.Index([i])
        out.append(line)
    out = pd.concat(out).T
    out.to_csv(output_file)
    print(f"Results saved to {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Run BIA measurement and save results to CSV."
    )
    parser.add_argument("--json", type=str, help="Path to JSON file with parameters")
    parser.add_argument(
        "--output", type=str, default="saved_test.csv", help="Output CSV file name"
    )

    # Add individual parameters for command-line input
    parser.add_argument("--height", type=float)
    parser.add_argument("--weight", type=float)
    parser.add_argument("--age", type=int)
    parser.add_argument("--gender", type=str)
    parser.add_argument("--left_arm_resistance", type=float)
    parser.add_argument("--left_arm_reactance", type=float)
    parser.add_argument("--right_arm_resistance", type=float)
    parser.add_argument("--right_arm_reactance", type=float)
    parser.add_argument("--left_leg_resistance", type=float)
    parser.add_argument("--left_leg_reactance", type=float)
    parser.add_argument("--right_leg_resistance", type=float)
    parser.add_argument("--right_leg_reactance", type=float)
    parser.add_argument("--left_body_resistance", type=float)
    parser.add_argument("--left_body_reactance", type=float)
    parser.add_argument("--right_body_resistance", type=float)
    parser.add_argument("--right_body_reactance", type=float)
    parser.add_argument("--left_trunk_resistance", type=float)
    parser.add_argument("--left_trunk_reactance", type=float)
    parser.add_argument("--right_trunk_resistance", type=float)
    parser.add_argument("--right_trunk_reactance", type=float)

    args = parser.parse_args()

    if args.json:
        with open(args.json, "r") as f:
            params = json.load(f)
    else:
        params = {
            k: v
            for k, v in vars(args).items()
            if k not in ["json", "output"] and v is not None
        }

    run_bia(params, args.output)


if __name__ == "__main__":
    main()
