function lexComparer(a: number[], b: number[]): number {
  const len = Math.min(a.length, b.length);
  for (let i = 0; i < len; i++) {
    if (a[i] !== b[i]) {
      return a[i]! - b[i]!;
    }
  }
  return a.length - b.length;
}

function toArray<T>(value: T | T[]): T[] {
  return Array.isArray(value) ? value : [value];
}

export function computeOrdering<T extends string>(
  original: T[],
  ordered: T[]
): number[] {
  return ordered
    .map((item) => original.indexOf(item))
    .filter((index) => index !== -1);
}

export function precomposeComparer<T, S>(
  comparer: (a: S, b: S) => number,
  transformer: (value: T) => S
) {
  return (a: T, b: T): number => comparer(transformer(a), transformer(b));
}

export function getComparer<T>(
  getPriorityKey: (value: T) => number | number[]
) {
  return precomposeComparer(lexComparer, (value: T): number[] =>
    toArray(getPriorityKey(value))
  );
}

export function getStrictIndexFinder<T>(
  values: T[],
  keyGetter: (value: T) => string = JSON.stringify
): (value: T) => number {
  const indexMap = new Map<string, number>();
  values.forEach((value, index) => {
    const key = keyGetter(value);
    // if (indexMap.has(key)) {
    //   throw new Error(`Duplicate key: ${key}.`);
    // }
    indexMap.set(key, index);
  });

  function findIndex(value: T) {
    const key = keyGetter(value);
    const index = indexMap.get(key);
    if (index == null) {
      throw new Error(`Key ${key} not found.`);
    }
    return index;
  }

  return findIndex;
}

export function getIndexFinder<T>(
  values: T[],
  keyGetter: (value: T) => string = JSON.stringify
): (value: T) => number {
  const strictIndexFinder = getStrictIndexFinder(values, keyGetter);
  return (value: T) => {
    try {
      return strictIndexFinder(value);
    } catch {
      return values.length; // default to last if not found
    }
  };
}

export function createSortComparerFromArray<T>(
  values: T[],
  keyGetter: (value: T) => string = JSON.stringify
) {
  return getComparer(getIndexFinder(values, keyGetter));
}

export function createSortComparerFromArrays<
  const T extends readonly unknown[]
>(
  valuesArrays: { [K in keyof T]: T[K][] },
  ordering?: number[],
  keyGetters?: Partial<{ [K in keyof T]: (value: T[K]) => string }>
) {
  const usedOrdering = ordering ?? [...Array(valuesArrays.length).keys()];
  const indexFinders = usedOrdering
    .map((order) => ({
      order,
      array: valuesArrays[order],
      keyGetter:
        keyGetters?.[order] ?? ((value: unknown) => JSON.stringify(value)),
    }))
    .map(({ order, array, keyGetter }) => ({
      index: order,
      indexFinder: getIndexFinder(array!, keyGetter),
    }));
  return getComparer((item: T) =>
    indexFinders.map(({ index, indexFinder }) => indexFinder(item[index]))
  );
}
