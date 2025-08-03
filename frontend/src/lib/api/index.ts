import axios, { AxiosError, type AxiosInstance, type AxiosRequestConfig } from "axios";
import { getJwtToken, refreshAccessToken } from "$lib/api/auth";
import { UsersApiRoute } from "$lib/api/routes/UserApiRoute";
import type { Cookies } from "@sveltejs/kit";
import { GameTypeApiRoute } from "$lib/api/routes/GameTypeApiRoute";
import { newApiError, newApiResponse } from "$lib/api/responses";

export async function getAxiosInstance(cookies: Cookies) {
	const axiosInstance = axios.create({
		baseURL: "http://localhost:8080",
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
		accessToken = await refreshAccessToken(cookies);
	}

	axiosInstance.interceptors.request.use((config) => {
		config.headers.Authorization = `Bearer ${accessToken}`;
		return config;
	});

	axiosInstance.interceptors.response.use(
		(response) => response,
		async (error) => {
			const originalRequest = error.config;

			if (error.response?.status === 401 && !originalRequest?._retry) {
				originalRequest._retry = true;

				try {
					const accessToken = await refreshAccessToken(cookies);
					originalRequest.headers.Authorization = `Bearer ${accessToken}`;
					return axiosInstance(originalRequest);
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
		baseURL: "http://localhost:8080",
		timeout: 5000,
		headers: {
			"Content-Type": "application/json",
		},
	});
}

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

export async function getHome(cookies: Cookies) {
	const axiosInstance = await getAxiosInstance(cookies);
	return await makeApiRequest<string>(axiosInstance, {
		method: "GET",
		url: "/",
	});
}

export const apiClient = {
	home: getHome,
	users: new UsersApiRoute(),
	gameTypes: new GameTypeApiRoute(),
};
