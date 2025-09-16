import type { AxiosError } from "axios";

// TODO: validate correct shape - maybe zod?
type ErrorDetailList = Array<{ loc: Array<string>; msg: string }>;
type ErrorDetail = ErrorDetailList | string;

const NO_DATA_AVAILABLE = { error: "No detail available" };

export abstract class ApiError extends Error {
	name = "ApiError";
	status: number = 500;
	protected readonly error: AxiosError;

	constructor(message: string, error: AxiosError) {
		super(message);
		this.error = error;
	}

	details = (): Record<string, string> => {
		return { TODO: `${this.name}.details() not implemented` };
	};

	protected parseDetails = (): ErrorDetail => {
		const data = this.error.response?.data;
		if (data === undefined) {
			throw new Error("error.response.data is undefined");
		}
		if (typeof data !== "object" || data === null || !("detail" in data)) {
			throw new Error("error.response.data.detail is undefined");
		}
		return data.detail as ErrorDetail;
	};
}

export class UnknownError extends ApiError {
	name = "UnknownError";
	status = 520;

	details = () => {
		return NO_DATA_AVAILABLE;
	};
}

export class BadRequestError extends ApiError {
	name = "BadRequestError";
	status = 400;

	details = () => {
		try {
			const detailsRaw = this.parseDetails() as string;
			const [err, detail] = detailsRaw.split(":");
			return { [err]: detail };
		} catch {
			return NO_DATA_AVAILABLE;
		}
	};
}

export class UnauthorizedError extends ApiError {
	name = "UnauthorizedError";
	status = 401;

	details = () => {
		try {
			const detailsRaw = this.parseDetails() as string;
			const [err, detail] = detailsRaw.split(":");
			return { [err]: detail };
		} catch {
			return NO_DATA_AVAILABLE;
		}
	};
}

export class NotEnoughPermissionError extends ApiError {
	name = "NotEnoughPermissionError";
	status = 403;
}

export class NotFoundError extends ApiError {
	name = "NotFoundError";
	status = 404;
}

export class UnprocessableDataError extends ApiError {
	name = "UnprocessableDataError";
	status = 422;

	details = () => {
		const detailsRaw = this.parseDetails() as ErrorDetailList; // TODO: validate correct shape
		const details: Record<string, string> = {};
		for (const detail of detailsRaw) {
			details[detail.loc[1]] = detail.msg;
		}
		return details;
	};
}

export class ServiceError extends ApiError {
	name = "ServiceError";

	details = () => {
		return { error: "This page was not found." };
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
	console.log(`api error: method=${error.request?.method} path=${error.request?.path} status=${status}`);

	const errorMap = new Map([
		[400, BadRequestError],
		[401, UnauthorizedError],
		[403, NotEnoughPermissionError],
		[404, NotFoundError],
		[422, UnprocessableDataError],
		[500, ServiceError],
	]);

	if (typeof status !== "number" || !errorMap.has(status)) {
		return new UnknownError(data, error);
	}

	const ApiErrorClass = errorMap.get(status)!;
	return new ApiErrorClass(data, error);
}
