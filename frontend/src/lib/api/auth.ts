import type { JWTToken } from "$lib/api/types/jwt";
import type { User, UserLogin } from "$lib/api/types/user";
import { type Cookies } from "@sveltejs/kit";
import { makeApiRequest, makeApiRequestUnauthorized, type Fetch } from "$lib/api/index";

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
	fetch: Fetch,
	cookies: Cookies,
	userLogin: UserLogin,
) {
	const params = new URLSearchParams();
	params.append("username", userLogin.username);
	params.append("password", userLogin.password);

	const jwtToken = await makeApiRequestUnauthorized<JWTToken>(fetch, "/auth/token", {
		method: "POST",
		body: params.toString(),
		headers: {
			"Content-Type": "application/x-www-form-urlencoded",
		},
	});
	setJwtToken(jwtToken, cookies);
}

export async function refreshAccessToken(fetch: Fetch, cookies: Cookies) {
	const jwtToken = await makeApiRequest<JWTToken>(fetch, cookies, "/auth/refresh", {
		method: "POST",
	});
	setJwtToken(jwtToken, cookies);
	return jwtToken.accessToken;
}

export async function readCurrentUser(fetch: Fetch, cookies: Cookies) {
	return await makeApiRequest<User>(fetch, cookies, "/auth/me", { method: "GET" });
}
