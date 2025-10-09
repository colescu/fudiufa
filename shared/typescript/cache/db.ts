import { openDB, type IDBPDatabase, type DBSchema } from "idb";

const DB_NAME = "CacheDB";
const STORE_NAME = "files";

interface CacheDB extends DBSchema {
  [STORE_NAME]: {
    key: string;
    value: { data: any; timestamp: number };
  };
}

let db: IDBPDatabase<CacheDB> | null = null;

async function getDB(): Promise<IDBPDatabase<CacheDB>> {
  if (!db) {
    db = await openDB<CacheDB>(DB_NAME, 1, {
      upgrade(database) {
        if (!database.objectStoreNames.contains(STORE_NAME)) {
          database.createObjectStore(STORE_NAME, { keyPath: "key" });
        }
      },
    });
  }
  return db;
}

export async function getFromDB(
  key: string
): Promise<{ data: any; timestamp: number } | undefined> {
  const database = await getDB();
  return database.get(STORE_NAME, key);
}

export async function putToDB(value: {
  key: string;
  data: any;
  timestamp: number;
}): Promise<void> {
  const database = await getDB();
  await database.put(STORE_NAME, value);
}
