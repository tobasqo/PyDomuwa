import { readCurrentUser } from "$lib/api/auth";
import { apiClient } from "$lib/api/client";

export const load = async ({ fetch, cookies }) => {
	await readCurrentUser(fetch, cookies).catch(() => {});

	const [gameTypes] = await Promise.all([apiClient.getAllGameTypes(fetch, cookies)]);

	return {
		// gameRooms: [],
		gameTypes,
	};
};
