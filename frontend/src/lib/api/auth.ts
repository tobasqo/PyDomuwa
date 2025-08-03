import type { JWTToken } from "$lib/api/types/jwt";
import type { User, UserLogin } from "$lib/api/types/user";
import { type Cookies } from "@sveltejs/kit";
import {
	getAxiosInstance,
	getFreshAxiosInstance,
	makeApiRequest,
} from "$lib/api/index";

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

export async function loginForAccessToken(userLogin: UserLogin, cookies: Cookies) {
	const axiosInstance = getFreshAxiosInstance();
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
}

export async function refreshAccessToken(cookies: Cookies) {
	const axiosInstance = getFreshAxiosInstance();
	const { data, error } = await makeApiRequest<JWTToken>(axiosInstance, {
		method: "POST",
		url: "/auth/refresh",
		withCredentials: true,
	});
	if (error !== null) {
		removeJwtToken(cookies);
		return error;
	}
	setJwtToken(data, cookies);
	return data.accessToken;
}

export async function readCurrentUser(cookies: Cookies) {
	const axiosInstance = await getAxiosInstance(cookies);
	return await makeApiRequest<User>(axiosInstance, { method: "GET", url: "/auth/me" });
}
