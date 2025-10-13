import { getJwtToken } from "$lib/api/auth";
import { error, redirect } from "@sveltejs/kit";
import { apiClient, getAxiosInstance } from "$lib/api";

export const load = async ({ cookies }) => {
	const axiosInstance = await getAxiosInstance(cookies);
	const homeApiResult = await apiClient.home(axiosInstance);
	const { error: homeError } = homeApiResult;
	if (homeError !== null) {
		console.error(homeError);
		throw error(homeError.status, homeError.message);
	}

	const jwtToken = getJwtToken(cookies);
	if (!jwtToken) {
		throw redirect(303, `/login`);
	}
	return { gameRooms: [] };
};
