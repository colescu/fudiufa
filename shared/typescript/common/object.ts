export function fromEntriesConst<
  T extends readonly (readonly [PropertyKey, any])[]
>(
  entries: T
): { [K in T[number][0]]: Extract<T[number], readonly [K, any]>[1] } {
  return Object.fromEntries(entries) as any;
}

export function keysConst<T extends object>(obj: T) {
  return Object.keys(obj) as (keyof T)[];
}

export function valuesConst<T extends object>(obj: T) {
  return Object.values(obj) as T[keyof T][];
}

export function entriesConst<T extends object>(
  obj: T
): readonly (readonly [keyof T, T[keyof T]])[] {
  return Object.entries(obj) as unknown as readonly (readonly [
    keyof T,
    T[keyof T]
  ])[];
}

export function pick<T, K extends keyof T>(
  obj: T,
  keys: readonly K[]
): Pick<T, K> {
  return fromEntriesConst(keys.map((key) => [key, obj[key]])) as Pick<T, K>;
}

export function cartesianProduct<T extends readonly unknown[][]>(
  ...arrays: T
): Array<{ [K in keyof T]: T[K] extends readonly (infer U)[] ? U : never }> {
  type ResultTuple = {
    [K in keyof T]: T[K] extends readonly (infer U)[] ? U : never;
  };
  let result: ResultTuple[] = [[]] as ResultTuple[];
  arrays.forEach((array) => {
    result = result.flatMap((prefix) =>
      array.map((item) => [...prefix, item] as ResultTuple)
    );
  });
  return result;
}

export function deepCopy<T>(object: T): T {
  return JSON.parse(JSON.stringify(object));
}

export function deepEqual(a: any, b: any): boolean {
  if (a === b) return true;

  if (a && b && typeof a === "object" && typeof b === "object") {
    if (Array.isArray(a) && Array.isArray(b)) {
      if (a.length !== b.length) return false;
      for (let i = 0; i < a.length; i++) {
        if (!deepEqual(a[i], b[i])) return false;
      }
      return true;
    }

    if (Array.isArray(a) !== Array.isArray(b)) return false;

    const keysA = Object.keys(a);
    const keysB = Object.keys(b);
    if (keysA.length !== keysB.length) return false;

    for (const key of keysA) {
      if (!Object.prototype.hasOwnProperty.call(b, key)) return false;
      if (!deepEqual(a[key], b[key])) return false;
    }
    return true;
  }

  return false;
}
