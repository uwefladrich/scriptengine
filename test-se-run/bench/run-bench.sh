#!/usr/bin/env bash
# Benchmark: se --parallel-io vs se (sequential)
# Usage: bash run-bench.sh <dir_with_nc_files> [iterations]
# Set BENCH_WORKDIR if /tmp is too small.
set -uo pipefail

SRCDIR=${1:?'Usage: run-bench.sh <dir_with_nc_files> [iterations]'}
N=${2:-5}
DIR=$(cd "$(dirname "$0")" && pwd)
W=${BENCH_WORKDIR:-${TMPDIR:-/tmp}/se-bench-$$}

command -v se >/dev/null || { echo "ERROR: se not in PATH" >&2; exit 1; }

# Pick 10 largest .nc files
mapfile -t FILES < <(find "$SRCDIR" -maxdepth 1 -name '*.nc' -size +1M -printf '%s %f\n' | sort -rn | head -10 | awk '{print $2}')
(( ${#FILES[@]} >= 5 )) || { echo "ERROR: need >=5 .nc files >1MB" >&2; exit 1; }

YAML_LIST=$(printf ", '%s'" "${FILES[@]}"); YAML_LIST="[${YAML_LIST:2}]"

mkdir -p "$W/src"
for f in "${FILES[@]}"; do [ -f "$W/src/$f" ] || cp "$SRCDIR/$f" "$W/src/"; done

cat > "$W/ctx.yml" <<EOF
- base.context:
    files: $YAML_LIST
    srcdir: "$W/src"
    workdir: "$W/run"
EOF

echo "se --parallel-io benchmark: ${#FILES[@]} files, $N iterations"
echo ""

TIMEFORMAT='%R'

time_copy() {
    rm -rf "$W/run"
    { time se --loglevel error $1 "$W/ctx.yml" "$DIR/bench-copy.yml" ; } 2>&1 | tail -1
}

time_move() {
    rm -rf "$W/run"
    se --loglevel error "$W/ctx.yml" "$DIR/bench-move-setup.yml" >/dev/null 2>&1
    { time se --loglevel error $1 "$W/ctx.yml" "$DIR/bench-move.yml" ; } 2>&1 | tail -1
}

median() { printf '%s\n' "$@" | sort -n | awk -v n=$# 'NR==int(n/2)+1{print}'; }

for op in copy move; do
    par=() seq=()
    fn="time_$op"

    $fn "" >/dev/null 2>&1 || true
    $fn "--parallel-io" >/dev/null 2>&1 || true

    for ((i=1; i<=N; i++)); do
        if (( i%2 )); then
            par+=("$($fn "--parallel-io")")
            seq+=("$($fn "")")
        else
            seq+=("$($fn "")")
            par+=("$($fn "--parallel-io")")
        fi
    done

    mp=$(median "${par[@]}"); ms=$(median "${seq[@]}")
    sp=$(awk "BEGIN{printf \"%.0f\", ($ms-$mp)/$ms*100}")
    printf "  %-10s  par=%ss  seq=%ss  speedup=%s%%\n" "base.$op" "$mp" "$ms" "$sp"
    printf "             all par: %s\n" "${par[*]}"
    printf "             all seq: %s\n" "${seq[*]}"
done

echo ""
rm -rf "$W"
