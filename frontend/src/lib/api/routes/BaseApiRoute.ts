import type { AxiosInstance } from "axios";
import { type ApiError, type ApiResult } from "$lib/api/responses";
import { makeApiRequest } from "$lib/api";

export type QueryParams = {
	page?: number;
	pageSize?: number;
};

export class BaseApiRoute<
	TCreate,
	TUpdate,
	TResponse,
	TQueryParams extends QueryParams = QueryParams,
> {
	routeUrl: string;

	constructor(routePath: string) {
		this.routeUrl = routePath;
	}

	getById = async (
		axiosInstance: AxiosInstance,
		modelId: number,
	): Promise<ApiResult<TResponse>> => {
		return await makeApiRequest<TResponse>(axiosInstance, {
			method: "GET",
			url: this.routeUrl + modelId,
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
		axiosInstance: AxiosInstance,
		params: TQueryParams | undefined = undefined,
	): Promise<ApiResult<TResponse[]>> => {
		const urlParams = this.makeGetAllParams(params);
		return await makeApiRequest<TResponse[]>(axiosInstance, {
			method: "GET",
			url: this.routeUrl,
			params: urlParams,
		});
	};

	create = async (
		axiosInstance: AxiosInstance,
		model: TCreate,
	): Promise<ApiResult<TResponse>> => {
		return await makeApiRequest<TResponse>(axiosInstance, {
			method: "POST",
			url: this.routeUrl,
			data: model,
		});
	};

	update = async (
		axiosInstance: AxiosInstance,
		modelId: number,
		model: TUpdate,
	): Promise<ApiResult<TResponse>> => {
		return await makeApiRequest<TResponse>(axiosInstance, {
			method: "PATCH",
			url: this.routeUrl + modelId,
			data: model,
		});
	};

	delete = async (
		axiosInstance: AxiosInstance,
		modelId: number,
	): Promise<ApiError | null> => {
		const { error } = await makeApiRequest(axiosInstance, {
			method: "DELETE",
			url: this.routeUrl + modelId,
		});
		return error;
	};
}
