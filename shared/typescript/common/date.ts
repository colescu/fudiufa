export function parseChineseDate(str: string): Date | undefined {
  const match = str
    .trim()
    .match(/(\d{4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日/);
  if (!match) return undefined;
  const [_, year, month, day] = match;
  return new Date(Number(year), Number(month) - 1, Number(day));
}

export function toChineseDate(date: Date | string): string {
  if (typeof date === "string") {
    date = new Date(date);
  }

  const parts = new Intl.DateTimeFormat("zh-CN", {
    year: "numeric",
    month: "numeric",
    day: "numeric",
  }).formatToParts(date);

  const year = parts.find((p) => p.type === "year")?.value ?? "";
  const month = parts.find((p) => p.type === "month")?.value ?? "";
  const day = parts.find((p) => p.type === "day")?.value ?? "";

  return `${year} 年 ${month} 月 ${day} 日`;
}
