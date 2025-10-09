import { getStrictIndexFinder } from "../common/sort";
import { fromEntriesConst } from "../common/object";

export function createConverter<R extends Record<string, unknown>>(
  data: R[],
  keyGetter: (value: unknown) => string = JSON.stringify
) {
  type Label = Extract<keyof R, string>;

  const indexMaps: {
    [K in Label]: (value: R[K]) => number;
  } = fromEntriesConst(
    (Object.keys(data[0]!) as Label[]).map((label) => [
      label,
      // LATERFIX allow non unique?
      // ipaStrict not unique for JP, VN
      getStrictIndexFinder(
        data.map((item) => item[label]),
        keyGetter
      ),
    ])
  );

  function convert<F extends Label, T extends Label>(
    value: R[F],
    from: F,
    to: T
  ): R[T] {
    return data[indexMaps[from](value)]![to];
  }

  return convert;
}
