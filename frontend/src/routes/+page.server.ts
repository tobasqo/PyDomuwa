import { getJwtToken } from "$lib/api/auth";
import { redirect } from "@sveltejs/kit";
import { apiClient, getAxiosInstance } from "$lib/api";

export const load = async ({ cookies }) => {
	const jwtToken = getJwtToken(cookies);
	if (!jwtToken) {
		console.log("Could not find token, redirecting to `/login`");
		throw redirect(303, `/login`);
	}
	const axiosInstance = await getAxiosInstance(cookies);
	const apiResult = await apiClient.gameTypes.getAll(axiosInstance);
	// TODO: add better error handling
	if (apiResult.error !== null) {
		redirect(303, "/login");
	}
	return apiResult.data;
};
