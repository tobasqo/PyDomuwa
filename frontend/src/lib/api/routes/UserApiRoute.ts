import { BaseApiRoute, handleServiceError } from "$lib/api/routes/BaseApiRoute";
import type { User, UserUpdate, UserCreate } from "$lib/api/types/user";
import type { AxiosInstance } from "axios";

export class UsersApiRoute extends BaseApiRoute<UserCreate, UserUpdate, User> {
	constructor() {
		super("/api/users/");
	}

	create = async (axiosInstance: AxiosInstance, model: UserCreate): Promise<User> => {
		try {
			const response = await axiosInstance.post<User>(this.routeUrl, model);
			return response.data;
		} catch (error) {
			throw handleServiceError(error);
		}
	};
}
