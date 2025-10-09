import { getMCQueryUtils, mcCache, MCEntry } from "@shared/mc";
import {
  entriesConst,
  fromEntriesConst,
  valuesConst,
} from "@shared/common/object";
import { ColumnData } from "../types";

function getTotalNumber(entries: MCEntry[]): number {
  return entries.map((entry) => entry.字數).reduce((val, acc) => acc + val, 0);
}

type RelatorData<X extends string, Y extends string> = Record<
  X,
  Record<Y, MCEntry[]>
>;

export class Relator<X extends string, Y extends string> {
  constructor(
    private readonly getX: (entry: MCEntry) => X,
    private readonly getY: (entry: MCEntry) => Y,
    private readonly getComment: (x: X, y: Y) => string
  ) {}

  private get data(): RelatorData<X, Y> {
    const data: RelatorData<X, Y> = {} as any;
    for (const [index, entry] of Object.entries(mcCache.get())) {
      const x = this.getX(entry),
        y = this.getY(entry);
      if (!(x in data)) {
        data[x] = {} as any;
      }
      if (!(y in data[x])) {
        data[x][y] = [];
      }
      data[x][y].push(entry);
    }
    return data;
  }

  get columnData(): ColumnData {
    const { indexOf } = getMCQueryUtils();
    return fromEntriesConst(
      entriesConst(this.data).map(([x, values]) => {
        const total = getTotalNumber(valuesConst(values).flat());
        return [
          x,
          entriesConst(values)
            .map(([y, entries]) => ({
              value: y,
              frequency: getTotalNumber(entries) / total,
              comment: this.getComment(x, y as Y),
              mcIndices: entries.map((entry) => indexOf(entry)!),
            }))
            .sort((pos1, pos2) => pos2.frequency - pos1.frequency),
        ];
      })
    );
  }
}
