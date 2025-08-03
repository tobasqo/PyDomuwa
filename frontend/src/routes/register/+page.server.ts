import { type Actions, error, fail, redirect } from "@sveltejs/kit";
import { apiClient, getFreshAxiosInstance } from "$lib/api";

export const actions = {
	default: async ({ request }) => {
		const formData = await request.formData();
		const axiosInstance = getFreshAxiosInstance();
		const { error: err } = await apiClient.users.create(axiosInstance, {
			username: formData.get("username")!.toString(),
			password: formData.get("password")!.toString(),
		});
		if (err !== null) {
			console.log("register api error:", err.message);
			console.log("register api details:", err.details());
			console.log(JSON.stringify(err.details()));
			if (err.status === 422 || err.status === 400) {
				return fail(err.status, { error: err.message, details: err.details() });
			} else {
				throw error(err.status, err);
			}
		}
		throw redirect(303, "/login");
	},
} satisfies Actions;
