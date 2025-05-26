import type { JWTToken } from "$lib/api/types/jwt";
import type { User, UserLogin } from "$lib/api/types/user";
import axios from "axios";
import type { Cookies } from "@sveltejs/kit";
import { getAxiosInstance } from "$lib/api/index";

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
	const axiosInstance = getAxiosInstance(cookies);
	const { data } = await axiosInstance.post<JWTToken>("/auth/token", userLogin, {
		headers: {
			"Content-Type": "application/x-www-form-urlencoded",
		},
	});
	// TODO: handle invalid data passed
	setJwtToken(data, cookies);
	// TODO: redirect to home
}

export async function refreshAccessToken(cookies: Cookies) {
	try {
		const { data } = await axios.post<JWTToken>("/auth/refresh", {
			withCredentials: true,
		});
		setJwtToken(data, cookies);
		return data.accessToken;
	} catch (error) {
		removeJwtToken(cookies);
		// TODO: redirect to login page
		throw error;
	}
}

// export async function readCurrentUser(cookies: Cookies) {
// 	const apiClient = createApiClient(cookies);
// 	return await apiClient.get<User>("/auth/me");
// }
