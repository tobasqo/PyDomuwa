import axios from "axios";
import { getJwtToken, refreshAccessToken } from "$lib/api/auth";

export const api_client = axios.create({
	baseURL: "http://localhost:8080",
	timeout: 5000,
	headers: {
		"Content-Type": "application/json",
	},
	withCredentials: true,
});

api_client.interceptors.request.use((config) => {
	const jwtToken = getJwtToken();
	if (jwtToken?.accessToken) {
		config.headers.Authorization = `Bearer ${jwtToken.accessToken}`;
	}
	return config;
});

api_client.interceptors.response.use(
	(response) => response,
	async (error) => {
		const originalRequest = error.config;

		if (error.response.status === 401 && !originalRequest?._retry) {
			originalRequest._retry = true;

			try {
				const accessToken = await refreshAccessToken();
				originalRequest.headers.Authorization = `Bearer ${accessToken}`;
				return api_client(originalRequest);
			} catch (refreshError) {
				return Promise.reject(refreshError);
			}
		}

		return Promise.reject(error);
	},
);

// TODO: clean up this mess
// let isRefreshing = false;
// let refreshSubscribers: ((accessToken: string) => void)[] = [];
//
// function subscribeTokenRefresh(callback: (accessToken: string) => void) {
// 	refreshSubscribers.push(callback);
// }
//
// function onTokenRefresh(accessToken: string) {
// 	refreshSubscribers.forEach((callback) => callback(accessToken));
// 	refreshSubscribers = [];
// }
//
// api_client.interceptors.response.use(
// 	(response) => response,
// 	async (error) => {
// 		const originalRequest = error.config;
//
// 		if (error.response?.status === 401 && !originalRequest._retry) {
// 			originalRequest._retry = true;
//
// 			if (!isRefreshing) {
// 				try {
// 					const newAccessToken = await refreshAccessToken();
// 					isRefreshing = true;
// 					onTokenRefresh(newAccessToken);
// 					return api_client(originalRequest);
// 				} catch (refreshError) {
// 					isRefreshing = false;
// 					refreshSubscribers = [];
// 					return Promise.reject(refreshError);
// 				}
// 			}
//
// 			return new Promise((resolve) => {
// 				subscribeTokenRefresh((accessToken: string) => {
// 					originalRequest.headers.Authorization = `Bearer ${accessToken}`;
// 					resolve(api_client(originalRequest));
// 				});
// 			});
// 		}
//
// 		return Promise.reject(error);
// 	},
// );
