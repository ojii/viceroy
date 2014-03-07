
describe("A suite", function() {
    it("contains spec with an expectation", function() {
        expect(true).toBe(true);
    });
    it("contains spec with an failing expectation", function() {
        expect(true).toBe(false);
    });
});
