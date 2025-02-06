import Axios, { type AxiosInstance } from "axios";

type HttpMethod = "get" | "post" | "put" | "delete";

class BaseApiRoute<TCreate, TUpdate, TResponse> {
	baseApiUrl = "http://localhost:8000/api/";
	routeUrl: string;
	client: AxiosInstance;

	constructor(routePath: string, accessToken: string | null = null) {
		this.routeUrl = this.baseApiUrl + routePath;
		this.client = this.createAxiosClient(this.routeUrl, accessToken);
	}

	createAxiosClient(routePath: string, accessToken: string | null) {
		return Axios.create({
			baseURL: routePath,
			responseType: "json" as const,
			headers: {
				"Content-Type": "application/json",
				...(accessToken && { Authorization: `Bearer ${accessToken}` }),
			},
		});
	}

	// makeApiCall = async (
	// 	endpoint: string,
	// 	method: HttpMethod,
	// 	payload: TCreate | TUpdate | null = null,
	// ) => {
	// 	try {
	// 		const response = await this.client[method](endpoint, payload);
	// 		return response.data;
	// 	} catch (error) {
	// 		handleServiceError(error);
	// 	}
	// 	return {} as TResponse;
	// };

	getById = async (modelId: number): Promise<TResponse> => {
		try {
			const response = await this.client.get<TResponse>(this.routeUrl + modelId);
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
			const response = await this.client.get<TResponse[]>(
				this.routeUrl + "?" + urlParams.toString(),
			);
			return response.data;
		} catch (error) {
			handleServiceError(error);
		}
		return {} as TResponse[];
	}

	async create(model: TCreate): Promise<TResponse> {
		try {
			const response = await this.client.post<TResponse>(this.routeUrl, model);
			return response.data;
		} catch (error) {
			handleServiceError(error);
		}
		return {} as TResponse;
	}

	async update(modelId: number, model: TUpdate): Promise<TResponse> {
		try {
			const response = await this.client.patch<TResponse>(this.routeUrl + modelId, model);
			return response.data;
		} catch (error) {
			handleServiceError(error);
		}
		return {} as TResponse;
	}

	async delete(modelId: number): Promise<void> {
		try {
			await this.client.patch<TResponse>(this.routeUrl + modelId);
		} catch (error) {
			handleServiceError(error);
		}
	}
}

function handleServiceError(error: any) {
	console.error(error);
	alert(error);
}
