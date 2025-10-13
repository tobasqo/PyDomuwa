import type { JWTToken } from "$lib/api/types/jwt";
import type { User, UserLogin } from "$lib/api/types/user";
import { type Cookies } from "@sveltejs/kit";
import { makeApiRequest } from "$lib/api/index";
import type { AxiosInstance } from "axios";

export function getJwtToken(cookies: Cookies) {
	const jwtToken = cookies.get("jwtToken");
	return jwtToken ? (JSON.parse(jwtToken) as JWTToken) : null;
}

export function setJwtToken(jwtToken: JWTToken, cookies: Cookies) {
	cookies.set("jwtToken", JSON.stringify(jwtToken), {
		path: "/",
		httpOnly: true,
		sameSite: "lax",
	});
}

export function removeJwtToken(cookies: Cookies) {
	cookies.delete("jwtToken", { path: "/" });
}

export async function loginForAccessToken(
	axiosInstance: AxiosInstance,
	userLogin: UserLogin,
	cookies: Cookies,
) {
	const { data, error } = await makeApiRequest<JWTToken>(axiosInstance, {
		method: "POST",
		url: "/auth/token",
		data: userLogin,
		headers: {
			"Content-Type": "application/x-www-form-urlencoded",
		},
	});
	if (error !== null) {
		return error;
	}
	setJwtToken(data, cookies);
	return null;
}

export async function refreshAccessToken(
	axiosInstance: AxiosInstance,
	cookies: Cookies,
) {
	const { data, error } = await makeApiRequest<JWTToken>(axiosInstance, {
		method: "POST",
		url: "/auth/refresh",
		withCredentials: true,
	});
	if (error !== null) {
		removeJwtToken(cookies);
		console.error("Failed to refresh access token:", error);
		return null;
	}
	setJwtToken(data, cookies);
	return data.accessToken;
}

export async function readCurrentUser(axiosInstance: AxiosInstance) {
	return await makeApiRequest<User>(axiosInstance, { method: "GET", url: "/auth/me" });
}
