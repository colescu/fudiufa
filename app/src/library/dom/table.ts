// Gets matrix of cells grouped by visual column
// (does not consider colspan)
export function getColumns(table: HTMLTableElement): HTMLElement[][] {
  const columns: HTMLElement[][] = [];
  const skip: number[] = [];

  for (let r = 0; r < table.rows.length; r++) {
    const row = table.rows[r];
    let colIndex = 0;

    Array.from(row!.cells).forEach((cell) => {
      while (skip[colIndex]! > 0) {
        skip[colIndex]!--;
        colIndex++;
      }

      (columns[colIndex] ||= []).push(cell);

      if (cell.rowSpan > 1) skip[colIndex] = cell.rowSpan - 1;

      colIndex++;
    });
  }

  return columns;
}

export function addClassToColumn(
  column: HTMLElement[],
  header: string,
  className: string
) {
  if (column[0]!.textContent === header) {
    column.slice(1).forEach((cell) => {
      cell.innerHTML = `<span class="${className}">${cell.textContent}</span>`;
    });
  }
}
