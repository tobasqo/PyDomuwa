import axios, { AxiosError, type AxiosInstance, type AxiosRequestConfig } from "axios";
import type { Cookies } from "@sveltejs/kit";
import { error, redirect } from "@sveltejs/kit";
import { getJwtToken, refreshAccessToken } from "$lib/api/auth";
import { UsersApiRoute } from "$lib/api/routes/UserApiRoute";
import { GameTypeApiRoute } from "$lib/api/routes/GameTypeApiRoute";
import { newApiError, newApiResponse, type ApiResult } from "$lib/api/responses";
import { QuestionApiRoute } from "$lib/api/routes/QuestionApiRoute";
import { GameCategoryApiRoute } from "$lib/api/routes/GameCategoryApiRoute";
import { QnACategoryApiRoute } from "$lib/api/routes/QnACategoryApiRoute";

const BASE_URL = "http://api:8000";

const requestRefresh = async(axiosInstance: AxiosInstance, refreshToken: string) => {
	const { data, error } = await makeApiRequest<JWTToken>(axiosInstance, {
		method: "POST",
		url: "/auth/refresh",
		withCredentials: true,
	});
}
export async function getAxiosInstance(cookies: Cookies) {
	return axios.create({
		baseURL: BASE_URL,
		timeout: 5000,
		headers: {
			"Content-Type": "application/json",
		},
		withCredentials: true,
	});
}

export async function getAxiosInstance(cookies: Cookies) {
	const axiosInstance = axios.create({
		baseURL: "http://api:8000",
		timeout: 5000,
		headers: {
			"Content-Type": "application/json",
		},
		withCredentials: true,
	});

	let accessToken = null;
	const jwtToken = getJwtToken(cookies);
	if (jwtToken !== null) {
		accessToken = jwtToken.accessToken;
	} else {
		// NOTE: throws
		accessToken = await refreshAccessToken(axiosInstance, cookies);
	}

	axiosInstance.interceptors.request.use((config) => {
		if (accessToken !== null) {
			config.headers.Authorization = `Bearer ${accessToken}`;
		}
		return config;
	});

	axiosInstance.interceptors.response.use(
		(response) => response,
		async (error) => {
			const originalRequest = error.config;

			if (error.response?.status === 401 && !originalRequest?._retry) {
				originalRequest._retry = true;

				try {
					const freshAxiosInstance = getFreshAxiosInstance();
					const accessToken = await refreshAccessToken(freshAxiosInstance, cookies);
					console.log("Refreshed access token:", accessToken);
					if (accessToken === null) {
						throw error(401, "Failed to refresh access token");
					}
					originalRequest.headers.Authorization = `Bearer ${accessToken}`;
					return freshAxiosInstance(originalRequest);
				} catch (refreshError) {
					return Promise.reject(refreshError);
				}
			}

			return Promise.reject(error);
		},
	);

	return axiosInstance;
}

export function getFreshAxiosInstance() {
	return axios.create({
		baseURL: "http://api:8000",
		timeout: 5000,
		headers: {
			"Content-Type": "application/json",
		},
	});
}

// axios-jwt or manually handle 401 and try refreshing token
export async function makeApiRequest<TResponse>(
	axiosInstance: AxiosInstance,
	config: AxiosRequestConfig = {},
) {
	return await axiosInstance
		.request<TResponse>(config)
		.then((res) => {
			return newApiResponse<TResponse>(res.data);
		})
		.catch((err) => {
			if (err instanceof AxiosError) {
				return newApiError<TResponse>(err);
			}
			console.error(err);
			throw err;
		});
}

export function handleApiResult<TResponse>(apiResult: ApiResult<TResponse>) {
	const { data, error: err } = apiResult;
	if (err !== null) {
		if (err.status === 401) {
			throw redirect(303, "/login");
		}
		throw error(err.status, err.message);
	}
	return data;
}

export async function getHome(axiosInstance: AxiosInstance) {
	return await makeApiRequest<string>(axiosInstance, {
		method: "GET",
		url: "/",
	});
}

export const apiClient = {
	home: getHome,
	users: new UsersApiRoute(),
	gameTypes: new GameTypeApiRoute(),
	gameCategories: new GameCategoryApiRoute(),
	qnaCategories: new QnACategoryApiRoute(),
	questions: new QuestionApiRoute(),
};
