import _ from "lodash";
import {
  useQuery,
  useMutation,
  useInfiniteQuery,
} from "react-query";
import useAppContext from "../hooks/useAppContext";

export function UseInfinateScroll(key, path, reactQueryOptions, defaultResponse) {
  const { fetchWithContext } = useAppContext();

  return useInfiniteQuery({
    queryKey: [path, ...key],
    queryFn: () => {
      if (path) {
        return fetchWithContext(path);
      } else {
        return Promise.resolve(defaultResponse);
      }
    },
    getNextPageParam: (lastPage, pages) => lastPage.nextCursor,
    ...reactQueryOptions,
  });
}

export function useFetch(key, path, reactQueryOptions, defaultResponse) {
  const { fetchWithContext } = useAppContext();

  return useQuery(
    [path, ...key],
    () => {
      if (path) {
        return fetchWithContext(path);
      } else {
        return Promise.resolve(defaultResponse);
      }
    },
    {
      keepPreviousData: true,
      ...reactQueryOptions,
    }
  );
}

export function useAction(path, method = "post", callbacks) {
  const { fetchWithContext } = useAppContext();
  return useMutation(
    (mutateParams) =>
      fetchWithContext(path, {
        method,
        headers: {
          "Content-Type": "application/json",
        },
        body: _.get(mutateParams, "body"),
      }),
    callbacks
  );
}
