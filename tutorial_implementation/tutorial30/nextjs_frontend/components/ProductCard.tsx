import Image from "next/image";

interface ProductCardProps {
  name: string;
  price: number;
  image: string;
  rating: number;
  inStock: boolean;
}

export function ProductCard(props: ProductCardProps) {
  return (
    <div className="border rounded-lg p-4 bg-card shadow-sm max-w-sm">
      <div className="relative w-full h-48 mb-3">
        <Image
          src={props.image}
          alt={props.name}
          fill
          sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
          className="rounded-md object-cover"
        />
      </div>
      <h3 className="font-semibold text-lg text-card-foreground">{props.name}</h3>
      <div className="flex items-center gap-2 mt-2">
        <span className="text-2xl font-bold text-green-600">
          ${props.price.toFixed(2)}
        </span>
        <span className="text-yellow-500">⭐ {props.rating.toFixed(1)}</span>
      </div>
      {props.inStock ? (
        <span className="inline-block mt-2 px-3 py-1 bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 rounded-full text-sm">
          In Stock
        </span>
      ) : (
        <span className="inline-block mt-2 px-3 py-1 bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200 rounded-full text-sm">
          Out of Stock
        </span>
      )}
    </div>
  );
}
