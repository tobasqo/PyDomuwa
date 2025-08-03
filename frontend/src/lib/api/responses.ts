import type { AxiosError } from "axios";

export abstract class ApiError extends Error {
	name = "ApiError";
	status: number;
	private error: AxiosError;

	protected constructor(message: string, status: number, error: AxiosError) {
		super(message);
		this.status = status;
		this.error = error;
	}

	abstract details(): Record<string, string>;
}

export class BadRequestError extends ApiError {
	name = "BadRequestError";

	constructor(message: string, error: AxiosError) {
		super(message, 400, error);
	}

	details = () => {
		const [err, detail] = this.error.response?.data.detail.split(":");
		return { [err]: detail };
	};
}

export class UnauthorizedError extends ApiError {
	name = "UnauthorizedError";

	constructor(message: string, error: AxiosError) {
		super(message, 401, error);
	}

	details = () => {
		const [err, detail] = this.error.response?.data.detail.split(":");
		return { [err]: detail };
	};
}

export class NotEnoughPermissionError extends ApiError {
	name = "NotEnoughPermissionError";

	constructor(message: string, error: AxiosError) {
		super(message, 403, error);
	}

	details = () => {
		return { TODO: `${this.name}.details() not implemented` };
	};
}

export class NotFoundError extends ApiError {
	name = "NotFoundError";

	constructor(message: string, error: AxiosError) {
		super(message, 404, error);
	}

	details = () => {
		return { TODO: `${this.name}.details() not implemented` };
	};
}

export class UnprocessableDataError extends ApiError {
	name = "UnprocessableDataError";

	constructor(message: string, error: AxiosError) {
		super(message, 422, error);
	}

	details = () => {
		const details: Record<string, string> = {};
		for (const detail of this.error.response?.data.detail) {
			details[detail.loc[1]] = detail.msg;
		}
		return details;
	};
}

export class ServiceError extends ApiError {
	name = "ServiceError";

	constructor(message: string, error: AxiosError) {
		super(message, 500, error);
	}

	details = () => {
		return { Error: "This page was not found." };
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
