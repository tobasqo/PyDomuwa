import { axios_instance } from "$lib/api";

export class BaseApiRoute<TCreate, TUpdate, TResponse> {
	routeUrl: string;

	constructor(routePath: string) {
		this.routeUrl = routePath;
	}

	getById = async (modelId: number): Promise<TResponse> => {
		try {
			const response = await axios_instance.get<TResponse>(this.routeUrl, {
				params: { model_id: modelId },
			});
			return response.data;
		} catch (error) {
			handleServiceError(error);
		}
		return {} as TResponse;
	};

	async getAll(page: number, pageSize: number): Promise<TResponse[]> {
		const urlParams = new URLSearchParams();
		urlParams.append("page", page.toString());
		urlParams.append("page_size", pageSize.toString());

		try {
			const response = await axios_instance.get<TResponse[]>(this.routeUrl, {
				params: urlParams,
			});
			return response.data;
		} catch (error) {
			handleServiceError(error);
		}
		return {} as TResponse[];
	}

	async create(model: TCreate): Promise<TResponse> {
		try {
			const response = await axios_instance.post<TResponse>(this.routeUrl, model);
			return response.data;
		} catch (error) {
			handleServiceError(error);
		}
		return {} as TResponse;
	}

	async update(modelId: number, model: TUpdate): Promise<TResponse> {
		try {
			const response = await axios_instance.patch<TResponse>(
				this.routeUrl + modelId,
				model,
			);
			return response.data;
		} catch (error) {
			handleServiceError(error);
		}
		return {} as TResponse;
	}

	async delete(modelId: number): Promise<void> {
		try {
			await axios_instance.patch<TResponse>(this.routeUrl + modelId);
		} catch (error) {
			handleServiceError(error);
		}
	}
}

function handleServiceError(error: any) {
	console.error(error);
	alert(error);
}
