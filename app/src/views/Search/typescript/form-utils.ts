import { fromEntriesConst } from "@shared/common/object";

export type Form<T> = {
  [K in keyof T]: T[K][];
};

// T: data type of form
// R: data type of database to search in
interface FormUtils<T, R> {
  readonly ITEMS: (keyof T)[];
  readonly EMPTY_FORM: Form<T>;
  readonly ALL_OPTIONS: Form<T>;

  getItemLabel?: { [K in keyof T]: (...rest: any[]) => string };
  getOptionLabel?: {
    [K in keyof T]: (...rest: any[]) => (option: string) => string;
  };

  toT: (entry: R) => T;

  getChecker: (form: Form<T>) => (entry: R) => boolean;

  computeOptions: (form: Form<T>) => Form<T>;
}

export function getFormUtils<T, R>(
  data: R[],
  getterMap: { [K in keyof T]: (entry: R) => T[K] },
  sorterMap?: { [K in keyof T]: (a: T[K], b: T[K]) => number }
): FormUtils<T, R> {
  const ITEMS = Object.keys(getterMap) as (keyof T)[];
  const ALL_OPTIONS = fromEntriesConst(
    ITEMS.map((item) => [
      item,
      [...new Set(data.map((entry) => getterMap[item](entry)))].sort(
        sorterMap?.[item]
      ),
    ])
  );

  function checkItem<K extends keyof T>(
    form: Form<T>,
    item: K,
    value: T[K]
  ): boolean {
    return form[item].length === 0 || form[item].includes(value);
  }

  return {
    ITEMS,
    ALL_OPTIONS,

    get EMPTY_FORM() {
      return fromEntriesConst(ITEMS.map((item) => [item, [] as unknown[]]));
    },

    toT(entry) {
      return fromEntriesConst(
        ITEMS.map((item) => [item, getterMap[item](entry)])
      ) as T;
    },

    getChecker(form) {
      return (entry) => {
        const t = this.toT(entry);
        return ITEMS.every((item) => checkItem(form, item, t[item]));
      };
    },

    // Gets the possible options based on the other items
    computeOptions(form) {
      const options: { [K in keyof T]: Set<T[K]> } = fromEntriesConst(
        ITEMS.map((item) => [item, new Set()])
      );

      for (const entry of data) {
        const t = this.toT(entry);

        let badItem: keyof T | null = null,
          bad = false;
        for (const item of ITEMS) {
          if (!checkItem(form, item, t[item])) {
            if (badItem === null) {
              badItem = item;
            } else {
              bad = true;
              break;
            }
          }
        }

        if (!bad) {
          if (badItem === null) {
            for (const item of ITEMS) {
              options[item].add(t[item]);
            }
          } else {
            options[badItem].add(t[badItem]);
          }
        }
      }

      return fromEntriesConst(
        ITEMS.map((item) => [
          item,
          ALL_OPTIONS[item].filter((option) => options[item].has(option)),
        ])
      );
    },
  };
}
