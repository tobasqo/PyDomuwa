import type { Cookies } from "@sveltejs/kit";
import { error, redirect } from "@sveltejs/kit";
import {
	getJwtToken,
	refreshAccessToken,
	removeJwtToken,
	setJwtToken,
} from "$lib/api/auth";

const BASE_URL = "http://api:8000";

export type Fetch = typeof globalThis.fetch;

export async function makeApiRequestUnauthorized(
	fetch: Fetch,
	path: string,
	options: RequestInit = {},
): Promise<Response> {
	const url = BASE_URL + path;
	const headers = new Headers(options.headers as HeadersInit);
	if (!headers.has("Content-Type")) {
		headers.set("Content-Type", "application/json");
	}

	const response = await fetch(url, {
		...options,
		headers,
		// credentials: "include",
	});
	return response;
}

export async function makeApiRequest(
	fetch: Fetch,
	cookies: Cookies,
	path: string,
	options: RequestInit = {},
): Promise<Response> {
	const url = BASE_URL + path;
	const jwtToken = getJwtToken(cookies);
	const headers = new Headers(options.headers as HeadersInit);
	if (!headers.has("Content-Type")) {
		headers.set("Content-Type", "application/json");
	}
	if (jwtToken === null) {
		throw redirect(303, "/login");
	}
	headers.set("Authorization", `Bearer ${jwtToken.accessToken}`);

	let response = await fetch(url, {
		...options,
		headers,
		credentials: "include",
	});
	if (response.status === 401) {
		removeJwtToken(cookies);
		const accessToken = await refreshAccessToken(fetch, cookies);
		if (accessToken === null) {
			console.error("API request failed:", response.status, response.statusText);
			removeJwtToken(cookies);
			throw error(401, "Unauthorized: Failed to refresh token");
		}
		jwtToken.accessToken = accessToken;
		setJwtToken(jwtToken, cookies);
		headers.set("Authorization", `Bearer ${accessToken}`);
		response = await fetch(url, {
			...options,
			headers,
			credentials: "include",
		});
	}
	return response;
}

export async function getHome(fetch: Fetch, cookies: Cookies) {
	await makeApiRequest(fetch, cookies, "/", {
		method: "GET",
	});
}

