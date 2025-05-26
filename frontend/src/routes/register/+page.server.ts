import { type Actions, redirect } from "@sveltejs/kit";
import { apiClient, getAxiosInstance } from "$lib/api";

export const actions = {
	default: async ({ cookies, request }) => {
		const data = await request.formData();
		const axiosInstance = getAxiosInstance(cookies);
		await apiClient.users.create(axiosInstance, {
			username: data.get("username")!.toString(),
			password: data.get("password")!.toString(),
		});
		redirect(303, "/login");
	},
} satisfies Actions;
