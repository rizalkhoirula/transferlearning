import { mount } from '@vue/test-utils';
import Food from './food.vue'; // Assuming food.vue is in the same directory or path is adjusted

// Mocking global.fetch
global.fetch = jest.fn();

// Mocking URL.createObjectURL and URL.revokeObjectURL
global.URL.createObjectURL = jest.fn(blob => `blob:mockurl/${blob.name}`);
global.URL.revokeObjectURL = jest.fn();

// Mock console.error to avoid cluttering test output, can be asserted too
global.console.error = jest.fn();

describe('Food.vue', () => {
  let wrapper;

  beforeEach(() => {
    // Reset mocks before each test
    fetch.mockClear();
    global.URL.createObjectURL.mockClear();
    global.URL.revokeObjectURL.mockClear();
    global.console.error.mockClear();
    
    wrapper = mount(Food);
  });

  afterEach(() => {
    if (wrapper) {
      wrapper.unmount();
    }
  });

  describe('formatRecipeText method', () => {
    // Accessing the method via wrapper.vm (instance of the component)
    const formatRecipeText = (data) => wrapper.vm.formatRecipeText(data);

    it('formats complete data correctly', () => {
      const data = {
        predicted_food: "ayam_pop",
        llm_info: {
          recipe: {
            name: "Ayam Pop",
            ingredients: ["1 chicken", "2 spices"],
            steps: ["Cook chicken", "Add spices"]
          },
          calories: "300-400 calories",
          nutrition: { protein: "High", carbs: "Low" }
        }
      };
      const expected = {
        predicted_food: "ayam_pop",
        name: "Ayam Pop",
        ingredients: ["1 chicken", "2 spices"],
        steps: ["Cook chicken", "Add spices"],
        calories: "300-400 calories",
        nutrition: { Protein: "High", Carbs: "Low" } // Note: formatNutrition capitalizes keys
      };
      expect(formatRecipeText(data)).toEqual(expected);
    });

    it('handles missing llm_info gracefully', () => {
      const data = { predicted_food: "unknown_food" };
      const result = formatRecipeText(data);
      expect(result.name).toBe("Recipe name not available.");
      expect(result.ingredients).toEqual(["Ingredients not available."]);
      expect(result.steps).toEqual(["Steps not available."]);
      expect(result.calories).toBe("Calories information not available.");
      expect(result.nutrition).toBeNull(); // or expect(result.nutrition).toEqual({ Information: "Not available" }); based on current implementation
      expect(wrapper.vm.error).toBe("LLM did not return sufficient recipe information."); // Check error set in component
    });
    
    it('handles missing recipe object', () => {
      const data = { llm_info: { calories: "100" } }; // No recipe
      const result = formatRecipeText(data);
      expect(result.name).toBe("Recipe name not available.");
      expect(result.ingredients).toEqual(["Ingredients not available."]);
      expect(result.steps).toEqual(["Steps not available."]);
      // Check error set in component if this case is considered an error
      expect(wrapper.vm.error).toBe("LLM did not return sufficient recipe information.");
    });

    it('handles missing individual recipe fields', () => {
      const data = {
        llm_info: {
          recipe: {}, // Empty recipe object
          calories: "250 calories",
        }
      };
      const result = formatRecipeText(data);
      expect(result.name).toBe("Recipe name not available.");
      expect(result.ingredients).toEqual(["Ingredients not available."]);
      expect(result.steps).toEqual(["Steps not available."]);
      expect(result.calories).toBe("250 calories");
       // Check error set in component if this case is considered an error
      expect(wrapper.vm.error).toBe("LLM did not return sufficient recipe information.");
    });
    
    it('handles empty ingredients and steps arrays', () => {
      const data = {
        llm_info: {
          recipe: { name: "Test Dish", ingredients: [], steps: [] },
        }
      };
      const result = formatRecipeText(data);
      expect(result.name).toBe("Test Dish");
      expect(result.ingredients).toEqual(["Ingredients not available."]);
      expect(result.steps).toEqual(["Steps not available."]);
    });

    it('handles missing calories', () => {
      const data = { llm_info: { recipe: { name: "Dish" } } };
      const result = formatRecipeText(data);
      expect(result.calories).toBe("Calories information not available.");
      expect(wrapper.vm.error).toBe("LLM did not return sufficient recipe information.");
    });

    it('handles missing nutrition object', () => {
      const data = { llm_info: { recipe: { name: "Dish" }, calories: "120" } }; // Nutrition missing
      const result = formatRecipeText(data);
      expect(result.nutrition).toBeNull();
    });
    
    it('returns null and sets error if data is null or undefined', () => {
        expect(formatRecipeText(null)).toBeNull();
        expect(wrapper.vm.error).toBe("No data received from server.");
        wrapper.vm.error = null; // Reset error for next check
        expect(formatRecipeText(undefined)).toBeNull();
        expect(wrapper.vm.error).toBe("No data received from server.");
    });

    it('handles nutrition data as a string', () => {
        const data = {
            llm_info: {
                recipe: { name: "Test Dish" },
                nutrition: "Generally healthy."
            }
        };
        const result = formatRecipeText(data);
        expect(result.nutrition).toEqual({ General: "Generally healthy." });
    });
  });

  describe('Image Preview Logic', () => {
    it('onFileChange sets imagePreviewUrl and selectedFile for a valid file', () => {
      const mockFile = new File(['dummy content'], 'example.png', { type: 'image/png' });
      const event = { target: { files: [mockFile] } };
      
      wrapper.vm.onFileChange(event);
      
      expect(wrapper.vm.selectedFile).toBe(mockFile);
      expect(wrapper.vm.imagePreviewUrl).toBe(`blob:mockurl/${mockFile.name}`);
      expect(global.URL.createObjectURL).toHaveBeenCalledWith(mockFile);
      expect(wrapper.vm.recipeInfo).toBeNull();
      expect(wrapper.vm.error).toBeNull();
    });

    it('onFileChange resets imagePreviewUrl and selectedFile if no file is selected', () => {
      // First set a file
      const mockFile = new File(['dummy content'], 'example.png', { type: 'image/png' });
      wrapper.vm.selectedFile = mockFile;
      wrapper.vm.imagePreviewUrl = 'blob:someurl';

      // Now simulate clearing the file input
      const event = { target: { files: [] } };
      wrapper.vm.onFileChange(event);
      
      expect(wrapper.vm.selectedFile).toBeNull();
      expect(wrapper.vm.imagePreviewUrl).toBeNull();
    });

    it('URL.revokeObjectURL is called when selectedFile changes (via watch)', async () => {
      const firstMockFile = new File(['first'], 'first.png', { type: 'image/png' });
      const secondMockFile = new File(['second'], 'second.png', { type: 'image/png' });
      
      // Set initial file and URL
      wrapper.vm.selectedFile = firstMockFile;
      wrapper.vm.imagePreviewUrl = 'blob:mockurl/first.png'; // Manually set for watch
      await wrapper.vm.$nextTick(); // Allow watcher to run if it hasn't

      // Simulate initial object URL creation for the first file
      global.URL.createObjectURL(firstMockFile); // call it so revoke has something to "revoke" in a real scenario

      // Change the file
      const event = { target: { files: [secondMockFile] } };
      wrapper.vm.onFileChange(event); // This will trigger the watcher due to selectedFile change
      await wrapper.vm.$nextTick();
      
      expect(global.URL.revokeObjectURL).toHaveBeenCalledWith('blob:mockurl/first.png');
      expect(wrapper.vm.imagePreviewUrl).toBe(`blob:mockurl/${secondMockFile.name}`);
    });

    it('URL.revokeObjectURL is called on unmount if imagePreviewUrl exists', () => {
      const mockFile = new File(['dummy'], 'test.png', { type: 'image/png' });
      wrapper.vm.selectedFile = mockFile; // Keep selectedFile in sync
      wrapper.vm.imagePreviewUrl = 'blob:mockurl/test.png'; // Set a mock URL
      
      wrapper.unmount();
      
      expect(global.URL.revokeObjectURL).toHaveBeenCalledWith('blob:mockurl/test.png');
    });
  });

  describe('uploadImage method', () => {
    const mockSuccessResponse = {
      predicted_food: "sushi",
      llm_info: {
        recipe: { name: "Sushi Roll", ingredients: ["rice", "nori", "fish"], steps: ["roll it"] },
        calories: "300",
        nutrition: { protein: "10g" }
      }
    };

    it('does nothing if no file is selected', async () => {
      wrapper.vm.selectedFile = null;
      await wrapper.vm.uploadImage();
      expect(fetch).not.toHaveBeenCalled();
    });

    it('calls fetch with FormData and sets recipeInfo and recipeTimestamp on successful response', async () => {
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockSuccessResponse,
      });
      
      const mockFile = new File(['sushi image'], 'sushi.jpg', { type: 'image/jpeg' });
      wrapper.vm.selectedFile = mockFile;
      
      await wrapper.vm.uploadImage();
      
      expect(fetch).toHaveBeenCalledTimes(1);
      expect(fetch).toHaveBeenCalledWith("/predict_food_class/", {
        method: "POST",
        body: expect.any(FormData), // Check that FormData was used
      });
      
      // Check if FormData contains the file
      const formData = fetch.mock.calls[0][1].body;
      expect(formData.get('file')).toBe(mockFile);

      expect(wrapper.vm.loading).toBe(false);
      expect(wrapper.vm.error).toBeNull();
      expect(wrapper.vm.recipeInfo.name).toBe("Sushi Roll");
      expect(wrapper.vm.recipeInfo.predicted_food).toBe("sushi");
      expect(wrapper.vm.recipeTimestamp).toMatch(/^\d{1,2}:\d{2}\s(AM|PM)$/); // e.g., 9:30 AM
    });

    it('handles fetch network error', async () => {
      fetch.mockRejectedValueOnce(new Error("Network failure"));
      
      wrapper.vm.selectedFile = new File(['dummy'], 'test.jpg');
      await wrapper.vm.uploadImage();
      
      expect(wrapper.vm.loading).toBe(false);
      expect(wrapper.vm.error).toBe("Error uploading image: Network failure");
      expect(wrapper.vm.recipeInfo).toBeNull();
      expect(wrapper.vm.recipeTimestamp).toBeNull();
      expect(console.error).toHaveBeenCalled();
    });

    it('handles non-ok HTTP response from fetch (JSON error message)', async () => {
      fetch.mockResolvedValueOnce({
        ok: false,
        status: 400,
        json: async () => ({ message: "Bad request from server" }),
      });
      
      wrapper.vm.selectedFile = new File(['dummy'], 'test.jpg');
      await wrapper.vm.uploadImage();
      
      expect(wrapper.vm.loading).toBe(false);
      expect(wrapper.vm.error).toBe("Error uploading image: Bad request from server");
      expect(wrapper.vm.recipeInfo).toBeNull();
      expect(wrapper.vm.recipeTimestamp).toBeNull();
      expect(console.error).toHaveBeenCalled();
    });

    it('handles non-ok HTTP response from fetch (non-JSON error message)', async () => {
        fetch.mockResolvedValueOnce({
          ok: false,
          status: 500,
          json: async () => { throw new Error("Cannot parse JSON") }, // Simulate JSON parsing error
        });
        
        wrapper.vm.selectedFile = new File(['dummy'], 'test.jpg');
        await wrapper.vm.uploadImage();
        
        expect(wrapper.vm.loading).toBe(false);
        expect(wrapper.vm.error).toBe("Error uploading image: Server error"); // Default message
        expect(wrapper.vm.recipeInfo).toBeNull();
        expect(wrapper.vm.recipeTimestamp).toBeNull();
        expect(console.error).toHaveBeenCalled();
      });

  });

  // Regarding "Chat Message Handling":
  // The component food.vue doesn't have generic addChatMessage or typeText methods.
  // The recipe display is styled like a chat message from a "Recipe Bot".
  // Tests for formatRecipeText and uploadImage (which sets recipeInfo and recipeTimestamp)
  // effectively cover the generation and data preparation for this "chat message".
  // No separate tests for non-existent generic chat methods will be added.
});
