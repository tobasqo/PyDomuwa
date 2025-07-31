import type { JWTToken } from "$lib/api/types/jwt";
import type { User, UserLogin } from "$lib/api/types/user";
import type { Cookies } from "@sveltejs/kit";
import { getAxiosInstance, getFreshAxiosInstance } from "$lib/api/index";

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
	const { data } = await axiosInstance.post<JWTToken>("/auth/token", userLogin, {
		headers: {
			"Content-Type": "application/x-www-form-urlencoded",
		},
	});
	// TODO: handle invalid data passed
	console.log("jwt data:", data);
	setJwtToken(data, cookies);
}

export async function refreshAccessToken(cookies: Cookies) {
	try {
		const axiosInstance = getFreshAxiosInstance();
		const { data } = await axiosInstance.post<JWTToken>("/auth/refresh", cookies, {
			withCredentials: true,
		});
		setJwtToken(data, cookies);
		return data.accessToken;
	} catch (error) {
		removeJwtToken(cookies);
		throw error;
	}
}

export async function readCurrentUser(cookies: Cookies) {
	const apiClient = await getAxiosInstance(cookies);
	return await apiClient.get<User>("/auth/me");
}
