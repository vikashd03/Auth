export interface Subscriber {
    id: string
    handler: (message: string) => void
}

export interface Topic {
    [name: string]: Subscriber[]
}

export interface User {
    id: number
    name: string
    email: string
}

export interface InitialState {
    access_token: string | null,
    user: User | null
}