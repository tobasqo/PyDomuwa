import { JWTTokenSchema, type JWTToken } from "$lib/api/types/jwt";
import { UserSchema, type UserLogin } from "$lib/api/types/user";
import { error, fail, type Cookies } from "@sveltejs/kit";
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

  const response = await makeApiRequestUnauthorized(fetch, "/auth/token", {
    method: "POST",
    body: params.toString(),
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  });
  const responseData = await response.json();
  if (!response.ok) {
    return fail(401, { details: responseData as string });
  }
  const jwtToken = JWTTokenSchema.safeParse(responseData);
  if (!jwtToken.success) {
    throw error(500, "Received malformed JWT token data from server.");
  }
  setJwtToken(jwtToken.data, cookies);
  return null;
}

export async function refreshAccessToken(fetch: Fetch, cookies: Cookies) {
  const response = await makeApiRequest(fetch, cookies, "/auth/refresh", {
    method: "POST",
  });
  const responseData = await response.json();
  const jwtToken = JWTTokenSchema.safeParse(responseData);
  if (!jwtToken.success) {
    throw error(500, "Received malformed JWT token data from server during refresh.");
  }
  setJwtToken(jwtToken.data, cookies);
  return jwtToken.data.accessToken;
}

export async function readCurrentUser(fetch: Fetch, cookies: Cookies) {
  const response = await makeApiRequest(fetch, cookies, "/auth/me", { method: "GET" });
  const responseData = await response.json();
  const user = UserSchema.safeParse(responseData);
  if (!user.success) {
    throw error(500, "Received malformed user data from server.");
  }
  return user.data;
}
