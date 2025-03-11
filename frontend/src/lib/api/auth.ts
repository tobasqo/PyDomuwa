import { axios_instance } from "$lib/api/index";
import type { JWTToken } from "$lib/api/types/jwt";
import type { User, UserLogin } from "$lib/api/types/user";
import axios from "axios";

// no local storage on the server, duh
class LocalStorage {
	data = {};

	getItem = (key: string) => {
		return this.data[key];
	};
	setItem = (key: string, value: any) => {
		return (this.data[key] = value);
	};
	removeItem = (key: string) => {
		delete this.data[key];
	};
}

const localStorage = new LocalStorage();

// TODO: add zod validation for all endpoints
export function getJwtToken() {
	const jwtToken = localStorage.getItem("jwtToken");
	return jwtToken ? (JSON.parse(jwtToken) as JWTToken) : null;
}

export function setJwtToken(jwtToken: JWTToken) {
	// TODO: get rid of storing refresh token in local storage
	localStorage.setItem("jwtToken", JSON.stringify(jwtToken));
}

export function removeJwtToken() {
	localStorage.removeItem("jwtToken");
}

export async function loginForAccessToken(userLogin: UserLogin) {
	const { data } = await axios_instance.post<JWTToken>("/auth/token", userLogin);
	setJwtToken(data);
	// TODO: redirect to home
}

export async function refreshAccessToken() {
	const jwtToken = getJwtToken();
	if (!jwtToken?.refreshToken) {
		removeJwtToken();
		// TODO: redirect to login page
		throw new Error("No refresh token available");
	}

	try {
		const { data } = await axios.post<JWTToken>("/auth/refresh", {
			refresh_token: jwtToken.refreshToken,
		});
		setJwtToken(data);
		return data.accessToken;
	} catch (error) {
		removeJwtToken();
		// TODO: redirect to login page
		throw error;
	}
}

export async function readCurrentUser() {
	return await axios_instance.get<User>("/auth/me");
}
