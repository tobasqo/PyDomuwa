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

export async function makeApiRequestUnauthorized<TResponse>(
	fetch: Fetch,
	path: string,
	options: RequestInit = {},
): Promise<TResponse> {
	const url = BASE_URL + path;
	const headers = new Headers(options.headers as HeadersInit);
	if (!headers.has("Content-Type")) {
		headers.set("Content-Type", "application/json");
	}

	let response = await fetch(url, {
		...options,
		headers,
		// credentials: "include",
	});
	if (!response.ok) {
		console.error("API request failed:", response.status, response.statusText);
		throw error(response.status, response.statusText);
	}

	return await response.json();
}

export async function makeApiRequest<TResponse>(
	fetch: Fetch,
	cookies: Cookies,
	path: string,
	options: RequestInit = {},
): Promise<TResponse> {
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
	if (!response.ok) {
		// TODO: add more details from response body
		// TODO: instead of throwing error, forward error to zod validation
		if (response.status === 422) {
			console.error(
				"API request validation error:",
				response.status,
				response.statusText,
			);
			// TODO: status should be included in output data
			return await response.json();
		}
		console.error("API request failed:", response.status, response.statusText);
		throw error(response.status, response.statusText);
	}

	return await response.json();
}

export async function getHome(fetch: Fetch, cookies: Cookies) {
	return await makeApiRequest<string>(fetch, cookies, "/", {
		method: "GET",
	});
}

