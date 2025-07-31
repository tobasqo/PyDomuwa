import { BaseApiRoute } from "$lib/api/routes/BaseApiRoute";
import type { User, UserUpdate, UserCreate } from "$lib/api/types/user";

export class UsersApiRoute extends BaseApiRoute<UserCreate, UserUpdate, User> {
	constructor() {
		super("/api/users/");
	}
}
