import type { AxiosError, AxiosInstance } from "axios";

export class ApiError extends Error {
	name = "ApiError";
	status: number;
	private error: AxiosError;

	constructor(message: string, status: number, error: AxiosError) {
		super(message);
		this.status = status;
		this.error = error;
	}

	abstract details(): string[];
}

export class BadRequestError extends ApiError {
	name = "BadRequestError";

	constructor(message: string, error: AxiosError) {
		super(message, 400, error);
	}

	details = (): string[] => {
		return [`TODO: ${this.name}.details() not implemented`];
	};
}

export class UnauthorizedError extends ApiError {
	name = "UnauthorizedError";

	constructor(message: string, error: AxiosError) {
		super(message, 401, error);
	}

	details = (): string[] => {
		return [`TODO: ${this.name}.details() not implemented`];
	};
}

export class NotEnoughPermissionError extends ApiError {
	name = "NotEnoughPermissionError";

	constructor(message: string, error: AxiosError) {
		super(message, 403, error);
	}

	details = (): string[] => {
		return [`TODO: ${this.name}.details() not implemented`];
	};
}

export class NotFoundError extends ApiError {
	name = "NotFoundError";

	constructor(message: string, error: AxiosError) {
		super(message, 404, error);
	}

	details = (): string[] => {
		return [`This page was not found.`];
	};
}

export class UnprocessableDataError extends ApiError {
	name = "UnprocessableDataError";

	constructor(message: string, error: AxiosError) {
		super(message, 422, error);
	}

	details = (): string[] => {
		const details: string[] = [];
		for (const detail of this.error.response?.data?.detail) {
			details.push(`Invalid input for ${detail.loc[1]}: ${detail.msg}`);
		}
		return details;
	};
}

export class ServiceError extends ApiError {
	name = "ServiceError";

	constructor(message: string, error: AxiosError) {
		super(message, 500, error);
	}

	details = (): string[] => {
		return [`This page was not found.`];
	};
}

export type ApiResult<TResponse> =
	| {
			data: TResponse;
			error: null;
	  }
	| {
			data: null;
			error: ApiError;
	  };

export function newApiResponse<TResponse>(
	responseData: TResponse,
): ApiResult<TResponse> {
	return { data: responseData, error: null };
}

export function newApiError<TResponse>(error: AxiosError): ApiResult<TResponse> {
	const apiError = getTypeOfApiError(error);
	return { data: null, error: apiError };
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
	): Promise<ApiResult<TResponse>> => {
		return await axiosInstance
			.get<TResponse>(this.routeUrl, {
				params: { model_id: modelId },
			})
			.then((response) => {
				return newApiResponse<TResponse>(response.data);
			})
			.catch((error) => {
				return newApiError<TResponse>(error);
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
		return await axiosInstance
			.get<TResponse[]>(this.routeUrl, {
				params: urlParams,
			})
			.then((response) => {
				return newApiResponse<TResponse[]>(response.data);
			})
			.catch((error) => {
				return newApiError<TResponse[]>(error);
			});
	};

	create = async (
		axiosInstance: AxiosInstance,
		model: TCreate,
	): Promise<ApiResult<TResponse>> => {
		return await axiosInstance
			.post<TResponse>(this.routeUrl, model)
			.then((response) => {
				return newApiResponse<TResponse>(response.data);
			})
			.catch((error) => {
				return newApiError<TResponse>(error);
			});
	};

	update = async (
		axiosInstance: AxiosInstance,
		modelId: number,
		model: TUpdate,
	): Promise<ApiResult<TResponse>> => {
		return await axiosInstance
			.patch<TResponse>(this.routeUrl + modelId, model)
			.then((response) => {
				return newApiResponse<TResponse>(response.data);
			})
			.catch((error) => {
				return newApiError<TResponse>(error);
			});
	};

	delete = async (
		axiosInstance: AxiosInstance,
		modelId: number,
	): Promise<ApiError | null> => {
		return await axiosInstance
			.patch<TResponse>(this.routeUrl + modelId)
			.then((response) => {
				return null;
			})
			.catch((error) => {
				return getTypeOfApiError(error);
			});
	};
}

export function getTypeOfApiError(error: AxiosError): ApiError {
	const status = error.status;
	const data = error.message;
	console.log(`${error.request?.method} ${error.request?.path} ${status}`);
	switch (status) {
		case 400:
			return new BadRequestError(data, error);
		case 401:
			return new UnauthorizedError(data, error);
		case 403:
			return new NotEnoughPermissionError(data, error);
		case 404:
			return new NotFoundError(data, error);
		case 422:
			return new UnprocessableDataError(data, error);
		case 500:
			return new ServiceError(data, error);
	}
	return new ServiceError(data, error);
}
