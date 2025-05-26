import { getJwtToken } from "$lib/api/auth";
import { redirect } from "@sveltejs/kit";
import { getHome } from "$lib/api";
import { getAxiosInstance } from "$lib/api";

export const load = async ({ cookies }) => {
	const jwtToken = getJwtToken(cookies);
	if (!jwtToken) {
		throw redirect(303, `/login`);
	}
	const apiClient = getAxiosInstance(cookies);
	return { data: await getHome(apiClient) };
};
