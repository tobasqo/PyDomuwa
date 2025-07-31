import { type Actions, error, redirect } from "@sveltejs/kit";
import { apiClient, getFreshAxiosInstance } from "$lib/api";
import { UnprocessableDataError } from "$lib/api/routes/BaseApiRoute";

export const actions = {
	default: async ({ request }) => {
		const data = await request.formData();
		const axiosInstance = getFreshAxiosInstance();
		const apiResult = await apiClient.users.create(axiosInstance, {
			username: data.get("username")!.toString(),
			password: data.get("password")!.toString(),
		});
		if (apiResult.error !== null && apiResult.error instanceof UnprocessableDataError) {
			// TODO: custom page for error
			error(422, JSON.stringify(apiResult.error.details()));
		} else {
			console.error(apiResult.error);
		}
		redirect(303, "/login");
	},
} satisfies Actions;
