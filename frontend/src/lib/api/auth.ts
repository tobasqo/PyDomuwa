import { api_client } from "$lib/api/index";
import type { JWTToken } from "$lib/api/types/jwt";
import type { User, UserCreate, UserUpdate } from "$lib/api/types/user";
import axios from "axios";

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

export async function loginForAccessToken() {
	const { data } = await api_client.post<JWTToken>("/auth/login");
	setJwtToken(data);
	return data.accessToken;
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

export async function readUser() {
	return await api_client.get<User>("/auth/me");
}

export async function createUser(userCreate: UserCreate) {
	return await api_client.post<User>("/auth/", userCreate);
}

export async function getAllUsers() {
	return await api_client.get<User[]>("/auth/");
}

export async function getUser(id: number) {
	return await api_client.get<User>(`/auth/${id}`);
}

export async function updateUser(id: number, userUpdate: UserUpdate) {
	return await api_client.patch(`/auth/${id}`, userUpdate);
}

export async function deleteUser(id: number) {
	return await api_client.delete(`/auth/${id}`);
}
