import { makeApiRequest, type Fetch } from "$lib/api";
import type { Cookies } from "@sveltejs/kit";

export type QueryParams = {
  page?: number;
  pageSize?: number;
};

export class BaseApiRoute<
  TCreate,
  TUpdate,
  TQueryParams extends QueryParams = QueryParams,
> {
  routeUrl: string;

  constructor(routePath: string) {
    this.routeUrl = routePath;
  }

  getById = async (fetch: Fetch, cookies: Cookies, modelId: number) => {
    return await makeApiRequest(fetch, cookies, this.routeUrl + modelId, {
      method: "GET",
    });
  };

  makeGetAllParams = (
    params: TQueryParams | undefined = undefined,
  ): URLSearchParams => {
    const urlParams = new URLSearchParams();
    urlParams.append("page", (params?.page ?? 1).toString());
    urlParams.append("page_size", (params?.pageSize ?? 25).toString());
    return urlParams;
  };

  getAll = async (
    fetch: Fetch,
    cookies: Cookies,
    params: TQueryParams | undefined = undefined,
  ) => {
    const urlParams = this.makeGetAllParams(params);
    const url = this.routeUrl + "?" + urlParams.toString();
    return await makeApiRequest(fetch, cookies, url, {
      method: "GET",
    });
  };

  create = async (fetch: Fetch, cookies: Cookies, model: TCreate) => {
    return await makeApiRequest(fetch, cookies, this.routeUrl, {
      method: "POST",
      body: JSON.stringify(model),
    });
  };

  update = async (fetch: Fetch, cookies: Cookies, modelId: number, model: TUpdate) => {
    return await makeApiRequest(fetch, cookies, this.routeUrl + modelId, {
      method: "PATCH",
      body: JSON.stringify(model),
    });
  };

  delete = async (fetch: Fetch, cookies: Cookies, modelId: number): Promise<void> => {
    await makeApiRequest(fetch, cookies, this.routeUrl + modelId, {
      method: "DELETE",
    });
  };
}
