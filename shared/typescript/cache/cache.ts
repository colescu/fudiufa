export function createCache<T, S = T, Args extends any[] = any[]>(
  fetcher: (...args: Args) => Promise<T>,
  preprocessor?: (data: T, args?: Args) => S | Promise<S>,
  keyGetter: (args: Args) => string = JSON.stringify
) {
  const cache = new Map<string, S>();
  const promises = new Map<string, Promise<S>>();

  async function getPromise(args: Args): Promise<S> {
    const data = await fetcher(...args);
    return preprocessor
      ? await preprocessor(data, args)
      : (data as unknown as S);
  }

  function get(...args: Args): S {
    const key = keyGetter(args);
    const value = cache.get(key);
    if (value === undefined) {
      throw new Error(
        `Cache not initiated for key ${key}. Call load first or use getAsync.`
      );
    }
    return value;
  }

  async function getAsync(...args: Args): Promise<S> {
    const key = keyGetter(args);
    if (cache.has(key)) {
      promises.delete(key);
      return cache.get(key)!;
    }
    // prevent race conditions
    if (!promises.has(key)) {
      const promise = getPromise(args);
      promises.set(key, promise);
      try {
        const result = await promise;
        cache.set(key, result);
        return result;
      } finally {
        promises.delete(key);
      }
    }
    return promises.get(key)!;
  }

  async function load(...args: Args): Promise<void> {
    await getAsync(...args);
  }

  async function loadAll(argsList: Args[]): Promise<void> {
    await Promise.all(argsList.map((args) => load(...args)));
  }

  function clear(...args: Args) {
    const key = keyGetter(args);
    cache.delete(key);
    promises.delete(key);
  }

  function clearAll() {
    cache.clear();
    promises.clear();
  }

  return { get, getAsync, load, loadAll, clear, clearAll };
}
