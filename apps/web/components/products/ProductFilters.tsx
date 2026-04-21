"use client";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Separator } from "@/components/ui/separator";
import { Slider } from "@/components/ui/slider";
import api from "@/lib/api";
import { formatPrice } from "@/lib/utils";
import { ProductFilters as Filters } from "@/types";
import { useEffect, useState } from "react";

interface ProductFiltersProps {
  filters: Filters;
  onFiltersChange: (filters: Filters) => void;
}

interface Category {
  category: string;
  subcategories: string[];
}

export function ProductFilters({
  filters,
  onFiltersChange,
}: ProductFiltersProps) {
  const [categories, setCategories] = useState<Category[]>([]);
  const [brands, setBrands] = useState<string[]>([]);
  const [priceRange, setPriceRange] = useState<[number, number]>([0, 3000]);

  useEffect(() => {
    fetchCategories();
    fetchBrands();
  }, []);

  const fetchCategories = async () => {
    try {
      const response = await api.get("/products/categories");
      if (response.data.success) {
        setCategories(response.data.categories);
      }
    } catch (error) {
      console.error("Failed to fetch categories:", error);
    }
  };

  const fetchBrands = async () => {
    try {
      const response = await api.get("/products/brands");
      if (response.data.success) {
        setBrands(response.data.brands);
      }
    } catch (error) {
      console.error("Failed to fetch brands:", error);
    }
  };

  const handleFilterChange = (key: keyof Filters, value: any) => {
    onFiltersChange({ ...filters, [key]: value });
  };

  const handlePriceChange = (value: number[]) => {
    setPriceRange([value[0], value[1]]);
    handleFilterChange("min_price", value[0]);
    handleFilterChange("max_price", value[1]);
  };

  const clearFilters = () => {
    setPriceRange([0, 3000]);
    onFiltersChange({});
  };

  const selectedCategory = categories.find(
    (cat) => cat.category === filters.category
  );

  return (
    <Card className="sticky top-20">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle>Фильтры</CardTitle>
          <Button variant="ghost" size="sm" onClick={clearFilters}>
            Сбросить
          </Button>
        </div>
      </CardHeader>

      <CardContent className="space-y-6">
        {/* Search */}
        <div className="space-y-2">
          <Label>Поиск</Label>
          <Input
            placeholder="Поиск товаров..."
            value={filters.search || ""}
            onChange={(e) => handleFilterChange("search", e.target.value)}
          />
        </div>

        <Separator />

        {/* Category */}
        <div className="space-y-2">
          <Label>Категория</Label>
          <Select
            value={filters.category || ""}
            onValueChange={(value) => {
              handleFilterChange("category", value);
              handleFilterChange("subcategory", undefined);
            }}
          >
            <SelectTrigger>
              <SelectValue placeholder="Все категории" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="All Categories">Все категории</SelectItem>
              {categories.map((category) => (
                <SelectItem key={category.category} value={category.category}>
                  {category.category}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        {/* Subcategory */}
        {selectedCategory && (
          <div className="space-y-2">
            <Label>Подкатегория</Label>
            <Select
              value={filters.subcategory || ""}
              onValueChange={(value) =>
                handleFilterChange("subcategory", value)
              }
            >
              <SelectTrigger>
                <SelectValue placeholder="Все подкатегории" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="All Subcategories">
                  Все подкатегории
                </SelectItem>
                {selectedCategory.subcategories.map((subcategory) => (
                  <SelectItem key={subcategory} value={subcategory}>
                    {subcategory}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        )}

        {/* Brand */}
        <div className="space-y-2">
          <Label>Бренд</Label>
          <Select
            value={filters.brand || ""}
            onValueChange={(value) => handleFilterChange("brand", value)}
          >
            <SelectTrigger>
              <SelectValue placeholder="Все бренды" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="All Brands">Все бренды</SelectItem>
              {brands.map((brand) => (
                <SelectItem key={brand} value={brand}>
                  {brand}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <Separator />

        {/* Price Range */}
        <div className="space-y-4">
          <Label>Диапазон цен</Label>
          <Slider
            value={priceRange}
            onValueChange={handlePriceChange}
            max={3000}
            min={0}
            step={50}
            className="w-full"
          />
          <div className="flex items-center justify-between text-sm text-muted-foreground">
            <span>{formatPrice(priceRange[0])}</span>
            <span>{formatPrice(priceRange[1])}</span>
          </div>
        </div>

        {/* Rating */}
        <div className="space-y-2">
          <Label>Минимальный рейтинг</Label>
          <Select
            value={filters.min_rating?.toString() || ""}
            onValueChange={(value) =>
              handleFilterChange(
                "min_rating",
                value ? parseFloat(value) : undefined
              )
            }
          >
            <SelectTrigger>
              <SelectValue placeholder="Любой рейтинг" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="Any Rating">Любой рейтинг</SelectItem>
              <SelectItem value="4">4+ звёзд</SelectItem>
              <SelectItem value="3">3+ звёзд</SelectItem>
              <SelectItem value="2">2+ звёзд</SelectItem>
              <SelectItem value="1">1+ звезда</SelectItem>
            </SelectContent>
          </Select>
        </div>

        {/* In Stock Only */}
        <div className="flex items-center space-x-2">
          <input
            type="checkbox"
            id="in-stock"
            checked={filters.in_stock_only || false}
            onChange={(e) =>
              handleFilterChange("in_stock_only", e.target.checked)
            }
            className="rounded border-gray-300"
          />
          <Label htmlFor="in-stock" className="text-sm">
            Только в наличии
          </Label>
        </div>
      </CardContent>
    </Card>
  );
}
