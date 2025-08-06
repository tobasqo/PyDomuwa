import { getJwtToken } from "$lib/api/auth";
import { error, redirect } from "@sveltejs/kit";
import { apiClient, getAxiosInstance } from "$lib/api";
import type { ApiResult } from "$lib/api/responses";

function handleApiResult<TResponse>(apiResult: ApiResult<TResponse>) {
	const { data, error: err } = apiResult;
	if (err !== null) {
		if (err.status === 401) {
			return redirect(303, "/login");
		}
		error(err.status, err.message);
	}
	return data;
}

export const load = async ({ cookies }) => {
	const jwtToken = getJwtToken(cookies);
	if (!jwtToken) {
		throw redirect(303, `/login`);
	}
	const axiosInstance = await getAxiosInstance(cookies);
	const apiResult = await apiClient.gameTypes.getAll(axiosInstance);
	const gameTypes = handleApiResult(apiResult);
	// TODO: set `gameTypes` on the store
	return { gameRooms: [], gameTypes: gameTypes };
};
