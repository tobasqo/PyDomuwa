import { readCurrentUser } from "$lib/api/auth";
import { apiClient } from "$lib/api";

export const load = async ({ fetch, cookies }) => {
	await readCurrentUser(fetch, cookies).catch(() => {});

	const [gameTypes] = await Promise.all([apiClient.gameTypes.getAll(fetch, cookies)]);

	return {
		// gameRooms: [],
		gameTypes,
	};
};
