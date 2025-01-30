import _ from "lodash";
import {
  useQuery,
  useMutation,
  useInfiniteQuery,
} from "@tanstack/react-query";
import useAppContext from "../hooks/useAppContext";

export function UseInfinateScroll(key, queryFunc, reactQueryOptions) {

  return useInfiniteQuery({
    queryKey: [key],
    queryFn: queryFunc,
    getNextPageParam: (lastPage, pages) =>{
      if (lastPage.page * lastPage.itemsPerPage >= lastPage.total) {
        return undefined;
      }
      return lastPage.page + 1;
    },
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
