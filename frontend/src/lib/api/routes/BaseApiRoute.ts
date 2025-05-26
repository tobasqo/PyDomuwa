import { type AxiosInstance } from "axios";

export class ApiError extends Error {
	constructor(message: string) {
		super(message);
		this.name = "ApiError";
	}
}

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
	): Promise<TResponse> => {
		try {
			const response = await axiosInstance.get<TResponse>(this.routeUrl, {
				params: { model_id: modelId },
			});
			return response.data;
		} catch (error) {
			throw handleServiceError(error);
		}
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
	): Promise<TResponse[]> => {
		const urlParams = this.makeGetAllParams(params);

		try {
			const response = await axiosInstance.get<TResponse[]>(this.routeUrl, {
				params: urlParams,
			});
			return response.data;
		} catch (error) {
			throw handleServiceError(error);
		}
	};

	create = async (axiosInstance: AxiosInstance, model: TCreate): Promise<TResponse> => {
		try {
			const response = await axiosInstance.post<TResponse>(this.routeUrl, model);
			return response.data;
		} catch (error) {
			throw handleServiceError(error);
		}
	};

	update = async (
		axiosInstance: AxiosInstance,
		modelId: number,
		model: TUpdate,
	): Promise<TResponse> => {
		try {
			const response = await axiosInstance.patch<TResponse>(
				this.routeUrl + modelId,
				model,
			);
			return response.data;
		} catch (error) {
			throw handleServiceError(error);
		}
	};

	delete = async (axiosInstance: AxiosInstance, modelId: number): Promise<void> => {
		try {
			await axiosInstance.patch<TResponse>(this.routeUrl + modelId);
		} catch (error) {
			throw handleServiceError(error);
		}
	};
}

export const handleServiceError = (error: any): never => {
	// TODO: fix handling error
	console.error("API Error:", JSON.stringify(error.response.data));
	throw new ApiError(error?.message ?? "Unknown error");
};
