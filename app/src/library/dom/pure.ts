export function computeGridOffset(
  totalItems: number,
  itemsPerRow: number
): number {
  const nextItemIndex = totalItems + 1;
  const remainder = nextItemIndex % itemsPerRow;
  const offset = (itemsPerRow - remainder) % itemsPerRow;
  return offset;
}

export function computeRowSpan<T>(
  data: T[][],
  decreasing: boolean = true
): number[][] {
  const rows = data.length;
  if (rows === 0) return [];
  const cols = data[0]!.length;

  const rowSpans: number[][] = Array(rows)
    .fill(0)
    .map(() => Array(cols).fill(1));
  const endRow: number[][] = Array.from({ length: rows }, () =>
    Array(cols).fill(0)
  );

  for (let col = 0; col < cols; col++) {
    let start = 0;
    while (start < rows) {
      let end = start + 1;
      while (
        end < rows &&
        data[end]![col] === data[start]![col] &&
        (!decreasing || col === 0 || end < endRow[start]![col - 1]!)
      ) {
        end++;
      }
      let span = end - start;

      rowSpans[start]![col] = span;
      for (let i = start; i < start + span; i++) {
        endRow[i]![col] = start + span;
      }
      for (let i = start + 1; i < end; i++) {
        rowSpans[i]![col] = 0;
      }
      start = end;
    }
  }

  return rowSpans;
}
