import axios, { type AxiosInstance } from "axios";
import { getJwtToken, refreshAccessToken } from "$lib/api/auth";
import { UsersApiRoute } from "$lib/api/routes/UserApiRoute";
import type { Cookies } from "@sveltejs/kit";

// TODO: we need to create axios instance per request on server side, with new cookies
export const getAxiosInstance = (cookies: Cookies) => {
	const axiosInstance = axios.create({
		baseURL: "http://localhost:8080",
		timeout: 5000,
		headers: {
			"Content-Type": "application/json",
		},
		withCredentials: true,
	});

	axiosInstance.interceptors.request.use((config) => {
		const jwtToken = getJwtToken(cookies);
		if (jwtToken?.accessToken) {
			config.headers.Authorization = `Bearer ${jwtToken.accessToken}`;
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
};

export async function getHome(axiosInstance: AxiosInstance) {
	const response = await axiosInstance.get<string>("/");
	return response.data;
}

export const apiClient = {
	users: new UsersApiRoute(),
};
